// מפיק את טוקן האימות מהסיסמה (אותה גזירה כמו בדפדפן ובשרת). הסיסמה עצמה לא נשמרת בשום מקום.
// שימוש: npm run token -- "הסיסמה-המשותפת"   ואז:  npx wrangler secret put AUTH_TOKEN
const crypto = require('crypto');
const pass = process.argv[2] || process.env.CHAT_PASSPHRASE;
if (!pass) { console.error('usage: npm run token -- "<passphrase>"'); process.exit(1); }
process.stdout.write(crypto.pbkdf2Sync(pass, 'love-chat-v1', 200000, 64, 'sha256').subarray(32).toString('hex') + '\n');
