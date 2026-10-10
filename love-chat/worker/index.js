// love-chat על Cloudflare Workers: רץ 24/7 בלי מחשב דולק.
// אותו פרוטוקול כמו server.js. השרת רואה רק מידע מוצפן (AES-GCM) - לא טקסט, לא תמונות, לא קול.
// Durable Object אחד ("החדר") מחזיק את חיבורי ה-WebSocket ואת ההיסטוריה המוצפנת ב-SQLite.
import { DurableObject } from 'cloudflare:workers';

const MAX_MESSAGES = 1500;
const MAX_CT = 950000;                 // הודעה בודדת - נכנס ב-frame אחד (מגבלה של 1MiB)
const MAX_TOTAL = 200 * 1024 * 1024;
const HISTORY_CHUNK = 700000;
const RATE_WINDOW_MS = 10000, RATE_MAX = 40, SIG_RATE_MAX = 300;
const BLOCK_AFTER = 8, BLOCK_MS = 10 * 60 * 1000;
const B64 = /^[A-Za-z0-9+/]+={0,2}$/;
const enc = new TextEncoder();

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname === '/ws') {
      if (req.headers.get('Upgrade') !== 'websocket') return new Response('expected websocket', { status: 426 });
      if (!/^[0-9a-f]{64}$/.test(env.AUTH_TOKEN || '')) return new Response('AUTH_TOKEN secret missing', { status: 500 });
      return env.CHAT.get(env.CHAT.idFromName('room')).fetch(req);
    }
    if (url.pathname === '/config.js') {
      let ice;
      try { ice = env.ICE_SERVERS ? JSON.parse(env.ICE_SERVERS) : undefined; } catch (e) {}
      const body = `window.CHAT_CONFIG = ${JSON.stringify({
        SERVER_URL: '', SAME_ORIGIN: true, WS_PATH: '/ws',
        SETUP: !/^[0-9a-f]{64}$/.test(env.AUTH_TOKEN || '') || undefined, // עדיין לא הוגדר טוקן - מסך הגדרה ראשונית
        GIPHY_KEY: env.GIPHY_KEY || '', OWNER_NAME: env.OWNER_NAME || 'ראובן',
        ICE_SERVERS: ice, TOGETHER_SINCE: env.TOGETHER_SINCE || undefined,
      })};\n`;
      return new Response(body, { headers: { 'Content-Type': 'application/javascript; charset=utf-8', 'Cache-Control': 'no-store' } });
    }
    if (url.pathname === '/health') return Response.json({ ok: true });
    return env.ASSETS.fetch(req);
  },
};

export class ChatRoom extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env);
    this.sql = ctx.storage.sql;
    this.sql.exec(`CREATE TABLE IF NOT EXISTS msgs (id TEXT PRIMARY KEY, ts INTEGER NOT NULL, iv TEXT NOT NULL, ct TEXT NOT NULL)`);
    this.sql.exec(`CREATE INDEX IF NOT EXISTS msgs_ts ON msgs(ts)`);
    this.sql.exec(`CREATE TABLE IF NOT EXISTS fails (ip TEXT PRIMARY KEY, count INTEGER NOT NULL, last INTEGER NOT NULL)`);
    // keepalive של הלקוח נענה בלי להעיר את ה-Durable Object (חוסך עלות)
    ctx.setWebSocketAutoResponse(new WebSocketRequestResponsePair('{"type":"ping"}', '{"type":"pong"}'));
    this.retentionMs = Number(env.RETENTION_DAYS || 3) * 86400000;
  }

  async fetch(req) {
    const [client, server] = Object.values(new WebSocketPair());
    this.ctx.acceptWebSocket(server);
    const now = Date.now();
    server.serializeAttachment({ authed: false, ip: req.headers.get('cf-connecting-ip') || '', rs: now, rn: 0, ss: now, sn: 0 });
    if (!(await this.ctx.storage.getAlarm())) await this.ctx.storage.setAlarm(now + 60 * 60 * 1000);
    return new Response(null, { status: 101, webSocket: client });
  }

  authed() { return this.ctx.getWebSockets().filter((w) => (w.deserializeAttachment() || {}).authed); }
  send(ws, obj) { try { ws.send(JSON.stringify(obj)); } catch (e) {} }
  broadcast(obj, except) {
    const s = JSON.stringify(obj);
    for (const w of this.authed()) if (w !== except) try { w.send(s); } catch (e) {}
  }

  blocked(ip) {
    const r = this.sql.exec('SELECT count, last FROM fails WHERE ip = ?', ip).toArray()[0];
    return r && r.count >= BLOCK_AFTER && Date.now() - r.last < BLOCK_MS;
  }
  fail(ip) {
    this.sql.exec(`INSERT INTO fails (ip, count, last) VALUES (?, 1, ?)
      ON CONFLICT(ip) DO UPDATE SET count = count + 1, last = excluded.last`, ip, Date.now());
  }

  async tokenOk(t) {
    if (typeof t !== 'string') return false;
    const a = enc.encode(t), b = enc.encode(this.env.AUTH_TOKEN || '');
    return a.byteLength === b.byteLength && b.byteLength > 0 && crypto.subtle.timingSafeEqual(a, b);
  }

  sendHistory(ws) {
    let batch = [], size = 0, first = true;
    const flush = (more) => { this.send(ws, { type: first ? 'history' : 'hist', msgs: batch, more }); first = false; batch = []; size = 0; };
    for (const m of this.sql.exec('SELECT id, ts, iv, ct FROM msgs ORDER BY ts, rowid')) {
      if (batch.length && size + m.ct.length > HISTORY_CHUNK) flush(true);
      batch.push({ id: m.id, ts: m.ts, iv: m.iv, ct: m.ct }); size += m.ct.length;
    }
    flush(false);
  }

  async webSocketMessage(ws, raw) {
    if (typeof raw !== 'string') raw = new TextDecoder().decode(raw);
    let m;
    try { m = JSON.parse(raw); } catch (e) { return; }
    if (!m || typeof m !== 'object') return;
    const st = ws.deserializeAttachment() || {};

    if (!st.authed) {
      if (this.blocked(st.ip)) { this.send(ws, { type: 'denied', reason: 'blocked' }); return ws.close(1008, 'blocked'); }
      if (m.type === 'auth' && (await this.tokenOk(m.token))) {
        st.authed = true; ws.serializeAttachment(st);
        this.sql.exec('DELETE FROM fails WHERE ip = ?', st.ip);
        this.sendHistory(ws);
        this.broadcast({ type: 'online', count: this.authed().length });
      } else {
        this.fail(st.ip);
        this.send(ws, { type: 'denied' });
        ws.close(1008, 'denied');
      }
      return;
    }

    const now = Date.now();
    if (m.type === 'ping') { this.send(ws, { type: 'pong' }); return; }

    // אותות שיחה/מצלמה: מוצפנים, לא נשמרים - רק מועברים לשאר המחוברים
    if (m.type === 'sig') {
      if (now - st.ss > RATE_WINDOW_MS) { st.ss = now; st.sn = 0; }
      st.sn++; ws.serializeAttachment(st);
      if (st.sn > SIG_RATE_MAX) return;
      if (typeof m.iv !== 'string' || m.iv.length !== 16 || !B64.test(m.iv)) return;
      if (typeof m.ct !== 'string' || !m.ct.length || m.ct.length >= 100000 || !B64.test(m.ct)) return;
      this.broadcast({ type: 'sig', iv: m.iv, ct: m.ct }, ws);
      return;
    }

    if (m.type === 'msg') {
      if (now - st.rs > RATE_WINDOW_MS) { st.rs = now; st.rn = 0; }
      st.rn++; ws.serializeAttachment(st);
      if (st.rn > RATE_MAX) return;
      if (typeof m.iv !== 'string' || m.iv.length !== 16 || !B64.test(m.iv)) return;
      if (typeof m.ct !== 'string' || !m.ct.length || m.ct.length >= MAX_CT || !B64.test(m.ct)) return;
      const msg = { id: crypto.randomUUID(), ts: now, iv: m.iv, ct: m.ct };
      this.sql.exec('INSERT INTO msgs (id, ts, iv, ct) VALUES (?, ?, ?, ?)', msg.id, msg.ts, msg.iv, msg.ct);
      this.trim();
      this.broadcast({ type: 'msg', msg });
    }
  }

  trim() {
    this.sql.exec(`DELETE FROM msgs WHERE rowid IN (SELECT rowid FROM msgs ORDER BY ts DESC, rowid DESC LIMIT -1 OFFSET ?)`, MAX_MESSAGES);
    let total = this.sql.exec('SELECT COALESCE(SUM(length(ct)), 0) AS n FROM msgs').one().n;
    while (total > MAX_TOTAL) {
      const r = this.sql.exec('SELECT rowid, length(ct) AS n FROM msgs ORDER BY ts, rowid LIMIT 1').toArray()[0];
      if (!r) break;
      this.sql.exec('DELETE FROM msgs WHERE rowid = ?', r.rowid); total -= r.n;
    }
  }

  async webSocketClose(ws) {
    const st = ws.deserializeAttachment() || {};
    try { ws.close(); } catch (e) {}
    if (st.authed) this.broadcast({ type: 'online', count: this.authed().filter((w) => w !== ws).length });
  }
  async webSocketError(ws) { await this.webSocketClose(ws); }

  // כל שעה: מחיקת הודעות וסטטוסים ישנים (ברירת מחדל 3 ימים) וניקוי חסימות שפגו
  async alarm() {
    const cutoff = Date.now() - this.retentionMs;
    const removed = this.sql.exec('DELETE FROM msgs WHERE ts < ?', cutoff).rowsWritten;
    if (removed) this.broadcast({ type: 'prune', before: cutoff });
    this.sql.exec('DELETE FROM fails WHERE last < ?', Date.now() - BLOCK_MS);
    await this.ctx.storage.setAlarm(Date.now() + 60 * 60 * 1000);
  }
}
