# Design sources

- `og.svg`: the source of `docs/assets/og.png`. Make the PNG again with
  `rsvg-convert -w 1200 -h 630 design/og.svg -o docs/assets/og.png`.
- `screens/`: the screenshots on the site. Each one copies the real dark-mode UI of the app
  with demo data for a made-up user "alex", so no real file name or path is in them. Run
  `python3 -I design/screens/gen_screens.py design/screens/out`, then
  `design/screens/render.sh` (needs Google Chrome). Update the HTML when the app UI changes.
