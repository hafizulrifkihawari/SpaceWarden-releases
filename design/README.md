# Design sources

- `mascot/`: the mascot, the favicon, the touch icon and the banner `og.png`. Run
  `python3 -I design/mascot/gen_mascot.py design/mascot`, then `design/mascot/render.sh`
  (needs Google Chrome). Small sizes (favicon, header) use the head only.
- `screens/`: the screenshots on the site. Each one copies the real dark-mode UI of the app
  with demo data for a made-up user "alex", so no real file name or path is in them. Run
  `python3 -I design/screens/gen_screens.py design/screens/out`, then
  `design/screens/render.sh` (needs Google Chrome). Update the HTML when the app UI changes.
