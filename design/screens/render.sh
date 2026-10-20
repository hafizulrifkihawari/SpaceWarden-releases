#!/bin/sh
# Renders the screen HTML files to 2x PNG files with a transparent background, then makes the
# animated SVG files of the overview and the storage map.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="$DIR/../../docs/assets"

# shot <html file> <png file>
shot() {
  "$CH" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --default-background-color=00000000 --window-size=1300,900 \
    --screenshot="$2" "file://$DIR/out/$1" 2>/dev/null
}

# boxes <name>: writes the boxes that out/<name>-base.html measures to out/<name>-boxes.json.
boxes() {
  "$CH" --headless=new --disable-gpu --window-size=1300,900 \
    --dump-dom "file://$DIR/out/$1-base.html" 2>/dev/null \
    | sed -n 's/.*<pre id="boxes" hidden="">\(.*\)<\/pre>.*/\1/p' | sed 's/&quot;/"/g' \
    > "$DIR/out/$1-boxes.json"
}

for name in overview storage-map duplicates media-library activity; do
  shot "$name.html" "$OUT/$name.png"
done

# The animated overview: a base image with no cards, one image for each card, the boxes of
# the cards, then the SVG that moves the cards with CSS animations.
shot overview-base.html "$DIR/out/overview-base.png"
for i in 1 2 3 4; do
  shot "overview-card$i.html" "$DIR/out/overview-card$i.png"
done
boxes overview
python3 -I "$DIR/gen_overview_anim.py" "$DIR/out" "$OUT/overview.svg"

# The animated storage map: a base image with no sunburst and no bars, the boxes of the
# sunburst and the bars, then the SVG that draws them with CSS animations.
shot storage-map-base.html "$DIR/out/storage-map-base.png"
boxes storage-map
python3 -I "$DIR/gen_storage_anim.py" "$DIR/out" "$OUT/storage-map.svg"

ls -la "$OUT"/overview.svg "$OUT"/storage-map.svg "$OUT"/overview.png "$OUT"/storage-map.png \
  "$OUT"/duplicates.png "$OUT"/media-library.png "$OUT"/activity.png
