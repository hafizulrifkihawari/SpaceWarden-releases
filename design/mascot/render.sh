#!/bin/sh
# Renders the mascot SVG files to the PNG files of the site, with Google Chrome.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="$DIR/../../docs/assets"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# render <svg> <png> <width> <height> <background>
render() {
  printf '<!doctype html><body style="margin:0"><img src="file://%s" width="%s" height="%s">' \
    "$DIR/$1" "$3" "$4" > "$TMP/page.html"
  "$CH" --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files \
    --default-background-color="$5" --window-size="$3,$4" \
    --screenshot="$OUT/$2" "file://$TMP/page.html" 2>/dev/null
}

render mascot.svg mascot-1024.png 1024 1024 00000000
render mascot.svg mascot-512.png 512 512 00000000
render mascot-head.svg mascot-head-256.png 256 256 00000000
render mascot-head.svg mascot-head-64.png 64 64 00000000
render mascot-head.svg favicon-32.png 32 32 00000000
render touch-icon.svg apple-touch-icon.png 180 180 ffffffff
render og.svg og.png 1200 630 ffffffff
ls -la "$OUT"/mascot-*.png "$OUT"/favicon-32.png "$OUT"/apple-touch-icon.png "$OUT"/og.png
