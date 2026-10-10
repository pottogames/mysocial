// מפעיל הכל בפקודה אחת: שרת הצ'אט + טונל Cloudflare + עדכון כתובת השרת באתר (GitHub Pages).
// הקישור של האתר נשאר קבוע; רק כתובת השרת מתעדכנת אוטומטית בכל הפעלה.
// האתר עצמו בודק מחדש את config.js כשהחיבור נופל, כך שגם דף פתוח יעבור לכתובת החדשה לבד.
const { spawn, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const { PORT } = require('./server.js');
let cfg = {};
try { cfg = JSON.parse(fs.readFileSync(path.join(__dirname, 'config.json'), 'utf8')); } catch (e) {}
const CONFIG_JS = path.join(__dirname, 'docs', 'config.js');
const isWin = process.platform === 'win32';
let lastUrl = '';
// טונל קבוע של Cloudflare (כתובת שלא משתנה). ראה README > "כתובת קבועה".
const TUNNEL_TOKEN = process.env.CF_TUNNEL_TOKEN || cfg.tunnelToken || '';
const PUBLIC_URL = (process.env.PUBLIC_URL || cfg.publicUrl || '').replace(/\/$/, '');
let backoff = 3000;

function git(args) {
  return spawnSync('git', args, { cwd: __dirname, encoding: 'utf8' });
}

function publish(url) {
  if (url === lastUrl) return;
  lastUrl = url;
  try { if (fs.readFileSync(CONFIG_JS, 'utf8').includes(JSON.stringify(url))) { console.log('כתובת השרת:', url); return; } } catch (e) {}
  const out = `window.CHAT_CONFIG = ${JSON.stringify({
    SERVER_URL: url,
    GIPHY_KEY: cfg.giphyKey || '',
    OWNER_NAME: cfg.ownerName || 'ראובן',
    ICE_SERVERS: cfg.iceServers || undefined,
    TOGETHER_SINCE: cfg.togetherSince || undefined,
  })};\n`;
  fs.writeFileSync(CONFIG_JS, out);
  console.log('כתובת השרת:', url);

  if (!fs.existsSync(path.join(__dirname, '.git'))) {
    console.log('(אין repo של git - דלג על העלאה ל-GitHub Pages)');
    return;
  }
  git(['add', 'docs/config.js']);
  const c = git(['commit', '-m', 'update server url']);
  if (c.status !== 0 && !/nothing to commit|nothing added/.test(c.stdout + c.stderr)) console.log(c.stderr);
  let p = git(['push']);
  if (p.status !== 0) {
    // אם ה-repo השתנה ב-GitHub (למשל עדכון מרחוק), מושכים ומנסים שוב
    git(['pull', '--rebase', '--autostash']);
    p = git(['push']);
  }
  console.log(p.status === 0 ? 'האתר עודכן ב-GitHub Pages (לוקח עד דקה)' : 'שגיאת push: ' + p.stderr);
}

function startTunnel() {
  const started = Date.now();
  const args = TUNNEL_TOKEN
    ? ['tunnel', '--no-autoupdate', 'run', '--token', TUNNEL_TOKEN]
    : ['tunnel', '--url', `http://localhost:${PORT}`, '--no-autoupdate'];
  const cf = spawn(isWin ? 'cloudflared.exe' : 'cloudflared', args, { stdio: ['ignore', 'pipe', 'pipe'] });
  const onData = (d) => {
    const m = String(d).match(/https:\/\/[a-z0-9-]+\.trycloudflare\.com/);
    if (m) publish(m[0]);
  };
  cf.stdout.on('data', onData);
  cf.stderr.on('data', onData);
  cf.on('error', () => console.error('cloudflared לא מותקן. ראה README.'));
  cf.on('exit', () => {
    // אם הטונל נופל מהר שוב ושוב, מחכים יותר בין ניסיונות (עד דקה)
    backoff = Date.now() - started > 60000 ? 3000 : Math.min(backoff * 2, 60000);
    console.log(`הטונל נפל, מרים מחדש בעוד ${Math.round(backoff / 1000)} שניות...`);
    setTimeout(startTunnel, backoff);
  });
}

if (PUBLIC_URL && !/^https:\/\//.test(PUBLIC_URL)) {
  console.error('publicUrl צריך להתחיל ב-https://');
  process.exit(1);
}
if (PUBLIC_URL) publish(PUBLIC_URL); // הכתובת קבועה - מעדכנים את האתר פעם אחת (ולא כלום אם לא השתנתה)
if (TUNNEL_TOKEN || !PUBLIC_URL) startTunnel();
else console.log('טונל קבוע רץ כשירות (cloudflared service) - לא מפעיל טונל מכאן');
process.on('uncaughtException', (e) => console.error('שגיאה:', e.message));
