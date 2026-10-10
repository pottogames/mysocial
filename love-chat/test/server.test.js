// בדיקת עשן: מריץ את השרת, מתחבר, מתאמת, שולח הודעה ובודק שהיא חוזרת ונשמרת.
const { test, before, after } = require('node:test');
const assert = require('node:assert');
const { spawn } = require('node:child_process');
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const WebSocket = require('ws');

const PASS = 'test-passphrase';
const PORT = 3900 + Math.floor(Math.random() * 90);
const DATA_DIR = fs.mkdtempSync(path.join(os.tmpdir(), 'love-chat-'));
const TOKEN = crypto.pbkdf2Sync(PASS, 'love-chat-v1', 200000, 64, 'sha256').subarray(32).toString('hex');
let proc;

before(async () => {
  proc = spawn(process.execPath, [path.join(__dirname, '..', 'server.js')], {
    env: { ...process.env, CHAT_PASSPHRASE: PASS, PORT: String(PORT), DATA_DIR },
    stdio: ['ignore', 'pipe', 'inherit'],
  });
  await new Promise((res) => proc.stdout.on('data', (d) => { if (/localhost/.test(d)) res(); }));
});
after(() => { proc.kill('SIGTERM'); });

function open() {
  const ws = new WebSocket(`ws://localhost:${PORT}`);
  const queue = [], waiters = [];
  ws.on('message', (d) => { const m = JSON.parse(d); const w = waiters.shift(); w ? w(m) : queue.push(m); });
  ws.next = (type) => new Promise(function get(res) {
    const take = (m) => (m.type === type ? res(m) : get(res));
    queue.length ? take(queue.shift()) : waiters.push(take);
  });
  return new Promise((res) => ws.on('open', () => res(ws)));
}

test('health and robots', async () => {
  assert.deepStrictEqual(await (await fetch(`http://localhost:${PORT}/health`)).json(), { ok: true });
  assert.match(await (await fetch(`http://localhost:${PORT}/robots.txt`)).text(), /Disallow: \//);
  assert.match(await (await fetch(`http://localhost:${PORT}/config.js`)).text(), /SAME_ORIGIN/);
});

test('wrong token is denied', async () => {
  const ws = await open();
  ws.send(JSON.stringify({ type: 'auth', token: 'nope' }));
  assert.strictEqual((await ws.next('denied')).type, 'denied');
});

test('auth, send, broadcast, persist', async () => {
  const a = await open(), b = await open();
  a.send(JSON.stringify({ type: 'auth', token: TOKEN }));
  b.send(JSON.stringify({ type: 'auth', token: TOKEN }));
  await a.next('history'); await b.next('history');

  const iv = crypto.randomBytes(12).toString('base64');
  const ct = crypto.randomBytes(40).toString('base64');
  a.send(JSON.stringify({ type: 'msg', iv, ct }));
  const got = await b.next('msg');
  assert.strictEqual(got.msg.ct, ct);

  // הודעה לא תקינה נזרקת
  a.send(JSON.stringify({ type: 'msg', iv: 'bad', ct: '<script>' }));
  a.send(JSON.stringify({ type: 'ping' }));
  await a.next('pong');

  await new Promise((r) => setTimeout(r, 500));
  const saved = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'messages.json'), 'utf8'));
  assert.strictEqual(saved.length, 1);
  assert.strictEqual(saved[0].ct, ct);
  a.close(); b.close();
});

test('call signals are relayed to the other side only, not stored', async () => {
  const a = await open(), b = await open();
  a.send(JSON.stringify({ type: 'auth', token: TOKEN }));
  b.send(JSON.stringify({ type: 'auth', token: TOKEN }));
  await a.next('history'); await b.next('history');
  const iv = crypto.randomBytes(12).toString('base64');
  const ct = crypto.randomBytes(64).toString('base64');
  a.send(JSON.stringify({ type: 'sig', iv, ct }));
  const got = await b.next('sig');
  assert.deepStrictEqual(got, { type: 'sig', iv, ct });
  // השולח לא מקבל את האות של עצמו
  a.send(JSON.stringify({ type: 'ping' }));
  assert.strictEqual((await a.next('pong')).type, 'pong');
  await new Promise((r) => setTimeout(r, 400));
  const saved = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'messages.json'), 'utf8'));
  assert.ok(!saved.some((m) => m.ct === ct));
  a.close(); b.close();
});
