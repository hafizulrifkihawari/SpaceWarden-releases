#!/bin/sh
# Renders the screen HTML files to 2x PNG files with a transparent background.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="$DIR/../../docs/assets"
for name in overview storage-map duplicates; do
  "$CH" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --default-background-color=00000000 --window-size=1300,900 \
    --screenshot="$OUT/$name.png" "file://$DIR/out/$name.html" 2>/dev/null
done
ls -la "$OUT"/overview.png "$OUT"/storage-map.png "$OUT"/duplicates.png
