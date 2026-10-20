"""Make the animated storage map, docs/assets/storage-map.svg.

The SVG holds the base screenshot (the storage map with no sunburst and no bars) and draws the
sunburst and the bars on it with CSS animations. First the sunburst grows ring by ring and the
bars grow. Then a pointer clicks Photos, the sunburst zooms into Photos, and a click on the
center zooms out again. This part repeats. With reduced motion, the SVG shows the still map.

The SVG has no script, so it works in an <img> tag. render.sh runs this script:

    python3 -I design/screens/gen_storage_anim.py design/screens/out docs/assets/storage-map.svg
"""
import base64
import json
import math
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
TARGET = Path(sys.argv[2])

data = json.loads((OUT / "storage-map.json").read_text())
boxes = json.loads((OUT / "storage-map-boxes.json").read_text())
base = base64.b64encode((OUT / "storage-map-base.png").read_bytes()).decode()

RINGS = data["rings"]
SIZE = 300
C = SIZE / 2
# The category that the pointer clicks.
PICK = 0
LOOP_S = 10
BUILD_S = 2.2


def arc(r0, r1, a0, a1, fill, extra=""):
    def pt(r, a):
        t = math.radians(a - 90)
        return C + r * math.cos(t), C + r * math.sin(t)
    # A full ring is two half arcs, because one arc cannot start and end at the same point.
    if a1 - a0 >= 359.99:
        return (arc(r0, r1, a0, a0 + 180, fill, extra)
                + arc(r0, r1, a0 + 180, a0 + 360, fill, extra))
    large = 1 if a1 - a0 > 180 else 0
    x0, y0 = pt(r1, a0); x1, y1 = pt(r1, a1); x2, y2 = pt(r0, a1); x3, y3 = pt(r0, a0)
    return (f'<path d="M{x0:.2f} {y0:.2f}A{r1} {r1} 0 {large} 1 {x1:.2f} {y1:.2f}'
            f'L{x2:.2f} {y2:.2f}A{r0} {r0} 0 {large} 0 {x3:.2f} {y3:.2f}Z" '
            f'fill="{fill}"{extra}/>')


def label(lines):
    ys = [C - 9, C + 6, C + 20]
    return "".join(f'<text x="{C}" y="{y}">{t}</text>' for y, t in zip(ys, lines))


segments = data["segments"]

# The whole sunburst, one group per category. Each segment grows in after a delay that goes
# out ring by ring and around the circle.
groups = {}
for cat, depth, a0, a1, fill in segments:
    delay = 0.1 + depth * 0.16 + a0 / 360 * 0.55
    groups.setdefault(cat, []).append(
        arc(*RINGS[depth], a0, a1, fill, f' style="--d:{delay:.2f}s"'))
whole = "".join(
    f'<g class="cat{" pick" if cat == PICK else " other"}">{"".join(paths)}</g>'
    for cat, paths in sorted(groups.items()))

# Photos zoomed in: its segments one ring further in, over the full circle.
p0, p1 = next((a0, a1) for cat, depth, a0, a1, _ in segments if cat == PICK and depth == 0)
zoom = "".join(
    arc(*RINGS[depth - 1], (a0 - p0) / (p1 - p0) * 360, (a1 - p0) / (p1 - p0) * 360, fill)
    for cat, depth, a0, a1, fill in segments if cat == PICK and depth >= 1)

pick = data["cats"][PICK]
sun = boxes["sunburst"][0]
sx, sy = sun["x"], sun["y"]

# Where the pointer goes, in the coordinates of the whole image: the middle of the inner
# Photos segment, then the center of the sunburst. It comes from the Photos row.
mid = math.radians((p0 + p1) / 2 - 90)
r_mid = (RINGS[0][0] + RINGS[0][1]) / 2
hit = (sx + C + r_mid * math.cos(mid), sy + C + r_mid * math.sin(mid))
center = (sx + C + 4, sy + C + 6)
row = boxes["rows"][PICK]
home = (row["x"] + 330, row["y"] + 70)


def at(p, s=1):
    return f"transform: translate({p[0]:.1f}px, {p[1]:.1f}px) scale({s})"


bars = "".join(
    f'<rect class="bar" x="{b["x"]}" y="{b["y"]}" width="{b["w"]}" height="{b["h"]}" rx="3" '
    f'fill="{c["color"]}" style="--d:{0.5 + i * 0.07:.2f}s"/>'
    for i, (b, c) in enumerate(zip(boxes["bars"], data["cats"])))

CSS = f"""
text {{ fill: #ececed; font: 11px -apple-system, BlinkMacSystemFont, sans-serif;
  text-anchor: middle; }}
.sun path {{ stroke: #27292d; stroke-width: 0.8; }}
.whole, .zoom, .whole .cat, .lab {{ transform-box: view-box; transform-origin: {C}px {C}px; }}
.zoom, .lab-pick, .cursor, .ring, .sel {{ opacity: 0; }}
.bar, .ring {{ transform-box: fill-box; }}
.bar {{ transform-origin: left center; }}
.ring {{ transform-origin: center; }}

@media (prefers-reduced-motion: no-preference) {{
  .whole path {{ animation: grow 0.8s cubic-bezier(0.2, 0.7, 0.2, 1) var(--d) backwards; }}
  .bar {{ animation: bar 0.9s cubic-bezier(0.2, 0.7, 0.2, 1) var(--d) backwards; }}
  .whole, .zoom, .other, .lab-all, .lab-pick, .cursor, .ring-a, .ring-b, .sel {{
    animation: {LOOP_S}s ease-in-out {BUILD_S}s infinite;
  }}
  .whole {{ animation-name: whole; }}
  .zoom {{ animation-name: zoom; }}
  .other {{ animation-name: dim; }}
  .lab-all {{ animation-name: lab-all; }}
  .lab-pick {{ animation-name: lab-pick; }}
  .cursor {{ animation-name: cursor; }}
  .ring-a {{ animation-name: ring-a; }}
  .ring-b {{ animation-name: ring-b; }}
  .sel {{ animation-name: sel; }}
}}

@keyframes grow {{ from {{ opacity: 0; transform: scale(0.6) rotate(-30deg); }} }}
@keyframes bar {{ from {{ transform: scaleX(0); }} }}

/* One loop of {LOOP_S} s. 25%: click on Photos. 59%: click on the center. */
@keyframes cursor {{
  0% {{ opacity: 0; {at(home)}; }}
  6% {{ opacity: 1; {at(home)}; }}
  21% {{ {at(hit)}; }}
  24% {{ {at(hit)}; }}
  25.5% {{ {at(hit, 0.85)}; }}
  27% {{ {at(hit)}; }}
  48% {{ {at(hit)}; }}
  57% {{ {at(center)}; }}
  58.5% {{ {at(center, 0.85)}; }}
  60% {{ {at(center)}; }}
  70% {{ opacity: 1; }}
  78% {{ opacity: 0; {at(home)}; }}
  100% {{ opacity: 0; {at(home)}; }}
}}
@keyframes ring-a {{
  0%, 25% {{ opacity: 0; transform: scale(0.3); }}
  25.5% {{ opacity: 0.8; transform: scale(0.3); }}
  31%, 100% {{ opacity: 0; transform: scale(2.6); }}
}}
@keyframes ring-b {{
  0%, 58.5% {{ opacity: 0; transform: scale(0.3); }}
  59% {{ opacity: 0.8; transform: scale(0.3); }}
  64.5%, 100% {{ opacity: 0; transform: scale(2.6); }}
}}
/* While the pointer is on Photos, the other categories get darker. */
@keyframes dim {{
  0%, 17% {{ opacity: 1; }}
  22%, 27% {{ opacity: 0.4; }}
  33%, 100% {{ opacity: 1; }}
}}
@keyframes whole {{
  0%, 26% {{ opacity: 1; transform: scale(1); }}
  33%, 58.5% {{ opacity: 0; transform: scale(1.35); }}
  66%, 100% {{ opacity: 1; transform: scale(1); }}
}}
@keyframes zoom {{
  0%, 26% {{ opacity: 0; transform: scale(0.55) rotate(-25deg); }}
  34%, 58.5% {{ opacity: 1; transform: scale(1) rotate(0deg); }}
  65%, 100% {{ opacity: 0; transform: scale(0.55) rotate(-25deg); }}
}}
@keyframes lab-all {{
  0%, 26% {{ opacity: 1; }}
  29%, 59% {{ opacity: 0; }}
  63%, 100% {{ opacity: 1; }}
}}
@keyframes lab-pick {{
  0%, 28% {{ opacity: 0; }}
  32%, 59% {{ opacity: 1; }}
  62%, 100% {{ opacity: 0; }}
}}
@keyframes sel {{
  0%, 26% {{ opacity: 0; }}
  30%, 58.5% {{ opacity: 1; }}
  63%, 100% {{ opacity: 0; }}
}}
"""

# The macOS arrow pointer. Its tip is at 0, 0.
CURSOR = ('<g class="cursor"><path d="M0 0V17.2L4.3 13.1L7.1 19.7L10 18.5L7.3 12H13.2Z" '
          'fill="#000" stroke="#fff" stroke-width="1.2" stroke-linejoin="round" '
          'filter="url(#shadow)"/></g>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1300" height="900" viewBox="0 0 1300 900">
<title>The SpaceWarden storage map</title>
<defs><filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
<feDropShadow dx="0" dy="1" stdDeviation="1.2" flood-opacity="0.5"/></filter></defs>
<style>{CSS}</style>
<image href="data:image/png;base64,{base}" width="1300" height="900"/>
<rect class="sel" x="{row["x"] - 6}" y="{row["y"]}" width="{row["w"] + 12}" height="{row["h"]}"
  rx="6" fill="#418ff8" fill-opacity="0.22"/>
{bars}
<svg class="sun" x="{sx}" y="{sy}" width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}"
  overflow="visible">
<g class="whole">{whole}</g>
<g class="zoom">{zoom}</g>
<circle cx="{C}" cy="{C}" r="33" fill="#2a2c2f"/>
<g class="lab lab-all">{label(["All", f'{data["total"]:.2f}', "GB"])}</g>
<g class="lab lab-pick">{label([pick["name"], f'{pick["gb"]:.2f}', "GB"])}</g>
</svg>
<circle class="ring ring-a" cx="{hit[0]:.1f}" cy="{hit[1]:.1f}" r="9" fill="none"
  stroke="#fff" stroke-width="1.5"/>
<circle class="ring ring-b" cx="{center[0]:.1f}" cy="{center[1]:.1f}" r="9" fill="none"
  stroke="#fff" stroke-width="1.5"/>
{CURSOR}
</svg>
'''
TARGET.write_text(svg)
print("wrote", TARGET, f"{len(svg) // 1024} KB")
