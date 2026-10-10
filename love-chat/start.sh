#!/usr/bin/env sh
# מקביל ל-start.bat עבור Mac/Linux: מריץ ומרים מחדש אם נפל
cd "$(dirname "$0")"
while true; do
  node run.js
  echo "השרת נפל, מפעיל מחדש בעוד 5 שניות..."
  sleep 5
done
