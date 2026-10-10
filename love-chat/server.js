// שרת צ'אט מוצפן. השרת לא רואה טקסט - רק מידע מוצפן (AES-GCM) שהלקוחות מצפינים.
const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const express = require('express');
const { WebSocketServer } = require('ws');

let cfg = {};
try { cfg = JSON.parse(fs.readFileSync(path.join(__dirname, 'config.json'), 'utf8')); } catch (e) {}
const PASSPHRASE = process.env.CHAT_PASSPHRASE || cfg.passphrase;
const PORT = Number(process.env.PORT || cfg.port || 3000);
const RETENTION_DAYS = Number(process.env.RETENTION_DAYS || cfg.retentionDays || 3);
const MAX_MESSAGES = 1500;
if (!PASSPHRASE) {
  console.error('חסרה סיסמה. צור config.json (ראה config.example.json)');
  process.exit(1);
}

// אותה גזירה בדיוק כמו בדפדפן: PBKDF2-SHA256, 200k, 64 בייט. חצי שני = טוקן אימות.
const SALT = 'love-chat-v1';
const AUTH_TOKEN = crypto.pbkdf2Sync(PASSPHRASE, SALT, 200000, 64, 'sha256').subarray(32).toString('hex');
const tokenBuf = Buffer.from(AUTH_TOKEN);

function tokenOk(t) {
  if (typeof t !== 'string') return false;
  const b = Buffer.from(t);
  return b.length === tokenBuf.length && crypto.timingSafeEqual(b, tokenBuf);
}

// שמירת הודעות (מוצפנות) לדיסק. כתיבה לקובץ זמני ואז rename, כדי שקריסה לא תשאיר קובץ פגום.
const DATA_DIR = process.env.DATA_DIR || path.join(__dirname, 'data');
const DATA_FILE = path.join(DATA_DIR, 'messages.json');
fs.mkdirSync(DATA_DIR, { recursive: true });
let messages = [];
try { messages = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8')); } catch (e) {}
if (!Array.isArray(messages)) messages = [];
let saveTimer = null;
function saveNow() {
  clearTimeout(saveTimer);
  saveTimer = null;
  const tmp = DATA_FILE + '.tmp';
  try {
    fs.writeFileSync(tmp, JSON.stringify(messages));
    fs.renameSync(tmp, DATA_FILE);
  } catch (e) { console.error('שגיאה בשמירה:', e.message); }
}
function save() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveNow, 300);
}

const app = express();
app.disable('x-powered-by');
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('X-Robots-Tag', 'noindex, nofollow, noarchive');
  res.setHeader('Referrer-Policy', 'no-referrer');
  next();
});
app.get('/robots.txt', (req, res) => res.type('text/plain').send('User-agent: *\nDisallow: /\n'));
app.get('/health', (req, res) => res.json({ ok: true }));
// גיבוי: האתר נגיש גם ישירות מכתובת השרת/הטונל (וגם מ-localhost לבדיקות).
// config.js נבנה כאן כך שהשרת הוא אותו מקור (SERVER_URL ריק = אותה כתובת).
app.get('/config.js', (req, res) => {
  res.type('application/javascript').setHeader('Cache-Control', 'no-store');
  res.send(`window.CHAT_CONFIG = ${JSON.stringify({
    SERVER_URL: '', SAME_ORIGIN: true, GIPHY_KEY: cfg.giphyKey || '', OWNER_NAME: cfg.ownerName || 'ראובן',
    ICE_SERVERS: cfg.iceServers || undefined,
  })};\n`);
});
app.use(express.static(path.join(__dirname, 'docs'), { index: 'index.html' }));
app.use((req, res) => res.status(404).end());

const server = http.createServer(app);
const wss = new WebSocketServer({ server, maxPayload: 256 * 1024 });

// הגבלת ניסיונות כושלים לפי IP
const fails = new Map();
const BLOCK_MS = 10 * 60 * 1000;
function blocked(ip) {
  const f = fails.get(ip);
  return f && f.count >= 8 && Date.now() - f.last < BLOCK_MS;
}
function fail(ip) {
  const f = fails.get(ip) || { count: 0, last: 0 };
  f.count++; f.last = Date.now();
  fails.set(ip, f);
}

function onlineCount() {
  let n = 0;
  for (const c of wss.clients) if (c.authed) n++;
  return n;
}
function broadcast(obj) {
  const s = JSON.stringify(obj);
  for (const c of wss.clients) if (c.authed && c.readyState === 1) c.send(s);
}

const B64 = /^[A-Za-z0-9+/]+={0,2}$/;
const RATE_WINDOW_MS = 10 * 1000;
const RATE_MAX = 40;
const SIG_RATE_MAX = 300;

wss.on('connection', (ws, req) => {
  const ip = req.headers['cf-connecting-ip'] || req.socket.remoteAddress;
  ws.authed = false;
  ws.alive = true;
  ws.rate = { start: Date.now(), n: 0 };
  ws.sigRate = { start: Date.now(), n: 0 };
  ws.on('pong', () => { ws.alive = true; });
  const authTimeout = setTimeout(() => { if (!ws.authed) ws.close(); }, 10000);

  ws.on('message', (raw) => {
    ws.alive = true;
    let m;
    try { m = JSON.parse(raw); } catch (e) { return; }
    if (!m || typeof m !== 'object') return;

    if (!ws.authed) {
      if (blocked(ip)) { ws.send(JSON.stringify({ type: 'denied', reason: 'blocked' })); return ws.close(); }
      if (m.type === 'auth' && tokenOk(m.token)) {
        ws.authed = true;
        clearTimeout(authTimeout);
        fails.delete(ip);
        ws.send(JSON.stringify({ type: 'history', msgs: messages }));
        broadcast({ type: 'online', count: onlineCount() });
      } else {
        fail(ip);
        ws.send(JSON.stringify({ type: 'denied' }));
        ws.close();
      }
      return;
    }

    if (m.type === 'ping') { ws.send(JSON.stringify({ type: 'pong' })); return; }

    // אותות לשיחת וידאו/קול (WebRTC). מוצפנים בדפדפן, לא נשמרים - רק מועברים לצד השני.
    if (m.type === 'sig') {
      const now = Date.now();
      if (now - ws.sigRate.start > RATE_WINDOW_MS) ws.sigRate = { start: now, n: 0 };
      if (++ws.sigRate.n > SIG_RATE_MAX) return;
      if (typeof m.iv !== 'string' || m.iv.length !== 16 || !B64.test(m.iv)) return;
      if (typeof m.ct !== 'string' || !m.ct.length || m.ct.length >= 100000 || !B64.test(m.ct)) return;
      const s = JSON.stringify({ type: 'sig', iv: m.iv, ct: m.ct });
      for (const c of wss.clients) if (c !== ws && c.authed && c.readyState === 1) c.send(s);
      return;
    }

    if (m.type === 'msg') {
      const now = Date.now();
      if (now - ws.rate.start > RATE_WINDOW_MS) ws.rate = { start: now, n: 0 };
      if (++ws.rate.n > RATE_MAX) return;
      if (typeof m.iv !== 'string' || m.iv.length !== 16 || !B64.test(m.iv)) return;
      if (typeof m.ct !== 'string' || !m.ct.length || m.ct.length >= 200000 || !B64.test(m.ct)) return;
      const msg = { id: crypto.randomUUID(), ts: now, iv: m.iv, ct: m.ct };
      messages.push(msg);
      if (messages.length > MAX_MESSAGES) messages = messages.slice(-MAX_MESSAGES);
      save();
      broadcast({ type: 'msg', msg });
    }
  });

  ws.on('close', () => {
    clearTimeout(authTimeout);
    if (ws.authed) broadcast({ type: 'online', count: onlineCount() });
  });
  ws.on('error', () => {});
});

// heartbeat: מנתק חיבורים "מתים" (טלפון שנכנס לשינה וכו') כדי שהנקודה הירוקה תהיה אמינה
const heartbeat = setInterval(() => {
  for (const ws of wss.clients) {
    if (!ws.alive) { ws.terminate(); continue; }
    ws.alive = false;
    try { ws.ping(); } catch (e) {}
  }
}, 30000);

// מחיקה אוטומטית של הודעות וסטטוסים ישנים (גם מהדיסק), וניקוי רשימת חסימות שפגו
function prune() {
  const cutoff = Date.now() - RETENTION_DAYS * 86400000;
  const before = messages.length;
  messages = messages.filter((m) => m.ts >= cutoff);
  if (messages.length !== before) {
    save();
    broadcast({ type: 'prune', before: cutoff });
    console.log(`נמחקו ${before - messages.length} רשומות ישנות (מעל ${RETENTION_DAYS} ימים)`);
  }
  for (const [ip, f] of fails) if (Date.now() - f.last > BLOCK_MS) fails.delete(ip);
}
prune();
const pruneTimer = setInterval(prune, 60 * 60 * 1000);

function shutdown() {
  clearInterval(heartbeat);
  clearInterval(pruneTimer);
  if (saveTimer) saveNow();
  process.exit(0);
}
process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);

server.listen(PORT, () => console.log(`שרת רץ על http://localhost:${PORT} , שומר ${RETENTION_DAYS} ימים אחורה`));
module.exports = { PORT, server, wss, AUTH_TOKEN };
