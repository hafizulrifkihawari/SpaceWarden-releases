"""Make the animated overview, docs/assets/overview.svg.

The SVG holds the base screenshot (the overview with no cards) and one image for each card of
Recommended Actions. First the cards fade in and rise, one after the other. Then a pointer
clicks the close button of "Remove old installers", that card fades out and the card under it
moves up. Later the card comes back. This part repeats. With reduced motion, the SVG shows the
still overview.

The SVG has no script, so it works in an <img> tag. render.sh runs this script:

    python3 -I design/screens/gen_overview_anim.py design/screens/out docs/assets/overview.svg
"""
import base64
import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
TARGET = Path(sys.argv[2])

boxes = json.loads((OUT / "overview-boxes.json").read_text())
cards = boxes["cards"]
closes = boxes["close"]
# The card that the pointer closes.
PICK = 2
LOOP_S = 10
BUILD_S = 1.6


def png(name):
    return "data:image/png;base64," + base64.b64encode((OUT / name).read_bytes()).decode()


x = closes[PICK]
hit = (x["x"] + x["w"] / 2, x["y"] + x["h"] / 2)
# The pointer tip stops a little above and left of the center of the button.
tip = (hit[0] - 2, hit[1] - 3)
home = (hit[0] - 260, cards[-1]["y"] + cards[-1]["h"] + 30)
lift = cards[PICK + 1]["y"] - cards[PICK]["y"]


def at(p, s=1):
    return f"transform: translate({p[0]:.1f}px, {p[1]:.1f}px) scale({s})"


layers = []
for i in range(len(cards)):
    cls = "pick" if i == PICK else ("below" if i > PICK else "")
    layers.append(f'<g class="rise" style="--d:{0.2 + i * 0.15:.2f}s">'
                  f'<image class="{cls}" href="{png(f"overview-card{i + 1}.png")}" '
                  f'width="1300" height="900"/></g>')

c = cards[PICK]
CSS = f"""
.pick {{ transform-box: view-box; transform-origin: {c["x"] + c["w"] / 2:.1f}px
  {c["y"] + c["h"] / 2:.1f}px; }}
.cursor, .ring, .hover {{ opacity: 0; }}
.ring {{ transform-box: fill-box; transform-origin: center; }}

@media (prefers-reduced-motion: no-preference) {{
  .rise {{ animation: rise 0.7s cubic-bezier(0.2, 0.7, 0.2, 1) var(--d) backwards; }}
  .pick, .below, .cursor, .ring, .hover {{
    animation: {LOOP_S}s ease-in-out {BUILD_S}s infinite;
  }}
  .pick {{ animation-name: pick; }}
  .below {{ animation-name: below; }}
  .cursor {{ animation-name: cursor; }}
  .ring {{ animation-name: ring; }}
  .hover {{ animation-name: hover; }}
}}

@keyframes rise {{ from {{ opacity: 0; transform: translateY(16px); }} }}

/* One loop of {LOOP_S} s. 25.5%: click on the close button. 80% to 90%: the card comes back. */
@keyframes cursor {{
  0% {{ opacity: 0; {at(home)}; }}
  6% {{ opacity: 1; {at(home)}; }}
  20% {{ {at(tip)}; }}
  24% {{ {at(tip)}; }}
  25.5% {{ {at(tip, 0.85)}; }}
  27% {{ {at(tip)}; }}
  36% {{ {at(tip)}; }}
  50% {{ opacity: 1; {at(home)}; }}
  56%, 100% {{ opacity: 0; {at(home)}; }}
}}
@keyframes hover {{
  0%, 19% {{ opacity: 0; }}
  22%, 27% {{ opacity: 1; }}
  30%, 100% {{ opacity: 0; }}
}}
@keyframes ring {{
  0%, 25.5% {{ opacity: 0; transform: scale(0.3); }}
  26% {{ opacity: 0.8; transform: scale(0.3); }}
  32%, 100% {{ opacity: 0; transform: scale(2.4); }}
}}
@keyframes pick {{
  0%, 26.5% {{ opacity: 1; transform: scale(1); }}
  31%, 84% {{ opacity: 0; transform: scale(0.97); }}
  90%, 100% {{ opacity: 1; transform: scale(1); }}
}}
@keyframes below {{
  0%, 29% {{ transform: translateY(0); }}
  36%, 80% {{ transform: translateY(-{lift:.1f}px); }}
  87%, 100% {{ transform: translateY(0); }}
}}
"""

# The macOS arrow pointer. Its tip is at 0, 0.
CURSOR = ('<g class="cursor"><path d="M0 0V17.2L4.3 13.1L7.1 19.7L10 18.5L7.3 12H13.2Z" '
          'fill="#000" stroke="#fff" stroke-width="1.2" stroke-linejoin="round" '
          'filter="url(#shadow)"/></g>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1300" height="900" viewBox="0 0 1300 900">
<title>The SpaceWarden Overview</title>
<defs><filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
<feDropShadow dx="0" dy="1" stdDeviation="1.2" flood-opacity="0.5"/></filter>
<clipPath id="content"><rect x="{c["x"]}" y="{cards[0]["y"] - 20}" width="{c["w"]}"
  height="{cards[-1]["y"] + cards[-1]["h"] - cards[0]["y"] + 40}"/></clipPath></defs>
<style>{CSS}</style>
<image href="{png("overview-base.png")}" width="1300" height="900"/>
<g clip-path="url(#content)">{"".join(layers)}</g>
<circle class="hover" cx="{hit[0]:.1f}" cy="{hit[1]:.1f}" r="11" fill="#fff" fill-opacity="0.12"/>
<circle class="ring" cx="{hit[0]:.1f}" cy="{hit[1]:.1f}" r="9" fill="none" stroke="#fff"
  stroke-width="1.5"/>
{CURSOR}
</svg>
'''
TARGET.write_text(svg)
print("wrote", TARGET, f"{len(svg) // 1024} KB")
