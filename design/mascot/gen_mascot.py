"""Make the SpaceWarden mascot: a fun cartoon warden with a vacuum cannon.

The mascot has no background and a white sticker outline, so it works on light and dark
pages. Run:

    python3 -I design/mascot/gen_mascot.py design/mascot
    design/mascot/render.sh

Outputs: mascot.svg (the full mascot), mascot-head.svg (the head only, for small sizes),
touch-icon.svg (the head on a light tile, for iOS) and og.svg (the 1200 x 630 banner).
"""
import math
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
INK = "#141418"
W = 16
O = f'stroke="{INK}" stroke-width="{W}" stroke-linejoin="round" stroke-linecap="round"'

BLUE, BLUE_SH, BLUE_LT = "#3a6fd8", "#24478f", "#6f9ff0"
SKIN, SKIN_SH = "#fcd9bd", "#eab394"
ORANGE, ORANGE_SH = "#ffad2e", "#d07a10"
TAN, TAN_SH = "#f0cf86", "#a77d3a"
STACHE = "#2b1d16"
GLOVE = "#ffffff"


def star(cx, cy, ro, ri, fill, sw=8):
    pts = []
    for i in range(10):
        r = ro if i % 2 == 0 else ri
        a = -math.pi / 2 + math.pi * i / 5
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return (f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{INK}" '
            f'stroke-width="{sw}" stroke-linejoin="round"/>')


def rope(d):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="34" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{TAN}" stroke-width="20" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{TAN_SH}" stroke-width="20" '
            f'stroke-dasharray="6 12"/>')


def body():
    return "".join([
        # Round little body.
        f'<path d="M262 980C250 860 320 780 420 770H560C660 780 730 860 718 980C600 1004 380 '
        f'1004 262 980Z" fill="{BLUE}" {O}/>',
        f'<path d="M300 900C312 840 350 806 400 792" fill="none" stroke="{BLUE_LT}" '
        f'stroke-width="18" stroke-linecap="round"/>',
        rope("M346 800C340 880 400 930 490 930C560 930 600 890 604 840"),
        f'<circle cx="490" cy="964" r="15" fill="{TAN}" stroke="{INK}" stroke-width="9"/>',
    ])


def thumbs_up():
    """The left arm, with a thumbs-up glove."""
    return "".join([
        f'<path d="M300 830C240 820 196 780 190 720" fill="none" stroke="{INK}" '
        f'stroke-width="96" stroke-linecap="round"/>',
        f'<path d="M300 830C240 820 196 780 190 720" fill="none" stroke="{BLUE}" '
        f'stroke-width="66" stroke-linecap="round"/>',
        # Cuff.
        f'<rect x="146" y="676" width="92" height="40" rx="14" fill="{GLOVE}" {O}/>',
        # Fist.
        f'<rect x="140" y="604" width="104" height="80" rx="30" fill="{GLOVE}" {O}/>',
        f'<path d="M150 630H234M150 656H234" stroke="{INK}" stroke-width="9" '
        f'stroke-linecap="round" opacity=".5"/>',
        # Thumb.
        f'<path d="M164 612C156 570 160 530 186 522C208 516 214 540 210 570L206 610" '
        f'fill="{GLOVE}" {O}/>',
    ])


def head():
    return "".join([
        # Big round face.
        f'<ellipse cx="440" cy="590" rx="172" ry="160" fill="{SKIN}" {O}/>',
        # Ears.
        f'<ellipse cx="272" cy="600" rx="30" ry="40" fill="{SKIN}" {O}/>',
        f'<ellipse cx="608" cy="600" rx="30" ry="40" fill="{SKIN}" {O}/>',
        # Cheeks.
        f'<ellipse cx="338" cy="640" rx="34" ry="20" fill="#ff8a8a" opacity=".55"/>',
        f'<ellipse cx="548" cy="640" rx="34" ry="20" fill="#ff8a8a" opacity=".55"/>',
        # Wink on the left.
        f'<path d="M352 564Q382 534 412 564" fill="none" stroke="{INK}" stroke-width="16" '
        f'stroke-linecap="round"/>',
        # Big eye on the right, with a raised brow.
        f'<ellipse cx="500" cy="556" rx="34" ry="42" fill="#fff" {O}/>',
        f'<circle cx="506" cy="562" r="20" fill="{INK}"/>',
        f'<circle cx="514" cy="552" r="7" fill="#fff"/>',
        # Big grin.
        f'<path d="M372 672Q440 700 518 668Q510 756 446 760Q382 756 372 672Z" fill="#8c1e2e" '
        f'{O}/>',
        f'<path d="M384 682Q440 704 506 680L502 700Q440 716 388 700Z" fill="#fff"/>',
        f'<ellipse cx="446" cy="740" rx="34" ry="16" fill="#ff6f7d"/>',
        f'<path d="M372 672Q440 700 518 668Q510 756 446 760Q382 756 372 672Z" fill="none" {O}/>',
        # Curly handlebar mustache.
        f'<path d="M444 662C404 630 350 630 322 654C300 672 268 668 258 640C252 616 276 598 '
        f'294 610C284 628 300 638 314 624C350 588 406 584 444 604C482 584 538 588 574 624'
        f'C588 638 604 628 594 610C612 598 636 616 630 640C620 668 588 672 566 654'
        f'C538 630 484 630 444 662Z" fill="{STACHE}" {O}/>',
        f'<path d="M352 616C376 606 404 606 424 612" fill="none" stroke="#6a4c3c" '
        f'stroke-width="8" stroke-linecap="round"/>',
        # Nose.
        f'<ellipse cx="444" cy="598" rx="32" ry="26" fill="#ffb592" {O}/>',
        f'<ellipse cx="434" cy="588" rx="10" ry="7" fill="#fff" opacity=".7"/>',
    ])


def helmet():
    parts = "".join([
        f'<path d="M282 462C270 280 352 158 450 152C548 158 630 280 618 462Z" fill="{BLUE}" {O}/>',
        f'<path d="M546 186C596 236 620 340 612 456H560C568 350 562 256 546 186Z" '
        f'fill="{BLUE_SH}" opacity=".5"/>',
        f'<path d="M340 420C334 320 360 250 404 206" fill="none" stroke="{BLUE_LT}" '
        f'stroke-width="22" stroke-linecap="round"/>',
        f'<rect x="430" y="112" width="40" height="44" rx="8" fill="{BLUE_SH}" {O}/>',
        f'<circle cx="450" cy="104" r="24" fill="{BLUE}" {O}/>',
        f'<path d="M236 448C300 430 600 430 664 448C680 486 640 506 450 506C260 506 220 486 '
        f'236 448Z" fill="{BLUE_SH}" {O}/>',
        f'<circle cx="450" cy="336" r="62" fill="{ORANGE}" {O}/>',
        f'<circle cx="450" cy="336" r="42" fill="none" stroke="{ORANGE_SH}" stroke-width="9" '
        f'stroke-dasharray="48 13"/>',
        star(450, 336, 34, 15, "#fff6d6"),
    ])
    return f'<g transform="rotate(-9 450 470)">{parts}</g>'


def cannon():
    parts = "".join([
        f'<rect x="0" y="-66" width="116" height="132" rx="44" fill="{BLUE_SH}" {O}/>',
        f'<path d="M26 -34V34" stroke="{BLUE_LT}" stroke-width="12" stroke-linecap="round"/>',
        f'<rect x="90" y="-50" width="290" height="100" rx="26" fill="#454955" {O}/>',
        f'<path d="M120 -28H350" stroke="#7a8090" stroke-width="12" stroke-linecap="round"/>',
        f'<rect x="160" y="-58" width="34" height="116" rx="9" fill="{ORANGE}" {O}/>',
        f'<rect x="300" y="-58" width="34" height="116" rx="9" fill="{ORANGE}" {O}/>',
        f'<path d="M376 -40L470 -100V100L376 40Z" fill="#33363f" {O}/>',
        f'<ellipse cx="470" cy="0" rx="26" ry="100" fill="#1b1c21" {O}/>',
        f'<ellipse cx="470" cy="0" rx="12" ry="62" fill="{ORANGE}"/>',
        f'<path d="M200 -50V-112H316V-50" fill="none" stroke="{INK}" stroke-width="40" '
        f'stroke-linejoin="round"/>',
        f'<path d="M200 -50V-112H316V-50" fill="none" stroke="{ORANGE}" stroke-width="22" '
        f'stroke-linejoin="round"/>',
        # Glove on the handle.
        f'<rect x="220" y="-150" width="86" height="84" rx="30" fill="{GLOVE}" {O}/>',
        f'<path d="M244 -140V-80M268 -142V-78" stroke="{INK}" stroke-width="8" '
        f'stroke-linecap="round" opacity=".45"/>',
    ])
    return f'<g transform="translate(560 900) rotate(-52) scale(.82)">{parts}</g>'


def doc(x, y, rot, s, kind):
    """A small file that flies into the cannon."""
    w, h = 64 * s, 80 * s
    c = 20 * s
    if kind == "photo":
        inner = (f'<rect x="{-w/2 + 10*s}" y="{-h/2 + 14*s}" width="{w - 20*s}" height="{h*0.5}" '
                 f'rx="4" fill="#7fd0ff"/><path d="M{-w/2 + 10*s} {-h/2 + 14*s + h*0.5}l{14*s} '
                 f'{-18*s} {10*s} {10*s} {8*s} {-8*s} {12*s} {16*s}Z" fill="#4caf50"/>')
    else:
        inner = "".join(f'<path d="M{-w/2 + 12*s} {-h/2 + (26 + i*14)*s}H{w/2 - 12*s}" '
                        f'stroke="#9aa3b5" stroke-width="{6*s}" stroke-linecap="round"/>'
                        for i in range(3))
    return (f'<g transform="translate({x} {y}) rotate({rot})">'
            f'<path d="M{-w/2} {-h/2}H{w/2 - c}L{w/2} {-h/2 + c}V{h/2}H{-w/2}Z" fill="#fff" '
            f'stroke="{INK}" stroke-width="{10*s}" stroke-linejoin="round"/>{inner}'
            f'<path d="M{w/2 - c} {-h/2}V{-h/2 + c}H{w/2}" fill="none" stroke="{INK}" '
            f'stroke-width="{8*s}" stroke-linejoin="round"/></g>')


def whoosh():
    lines = [
        "M890 250C880 340 850 420 820 500",
        "M960 360C920 420 880 470 850 520",
        "M770 200C790 300 800 400 800 480",
    ]
    out = "".join(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="12" '
                  f'stroke-linecap="round" stroke-dasharray="40 26"/>' for d in lines)
    files = (doc(900, 190, 24, 1.0, "doc") + doc(980, 300, -18, .85, "photo")
             + doc(770, 140, -12, .75, "doc"))
    sparkle = "".join(
        f'<path d="M{x} {y - r}Q{x} {y} {x + r} {y}Q{x} {y} {x} {y + r}Q{x} {y} {x - r} {y}'
        f'Q{x} {y} {x} {y - r}Z" fill="#ffd23f" stroke="{INK}" stroke-width="6" '
        f'stroke-linejoin="round"/>' for x, y, r in [(690, 230, 26), (1000, 470, 18),
                                                        (640, 140, 16)])
    return out + files + sparkle


def mascot():
    return (f'{whoosh()}{body()}{cannon()}{head()}{helmet()}{thumbs_up()}')


STICKER = ('<defs><filter id="st" x="-5%" y="-5%" width="110%" height="110%">'
           '<feMorphology in="SourceAlpha" operator="dilate" radius="12" result="d"/>'
           '<feFlood flood-color="#fff"/><feComposite in2="d" operator="in" result="w"/>'
           '<feMerge><feMergeNode in="w"/><feMergeNode in="SourceGraphic"/></feMerge>'
           '</filter></defs>')


def full():
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" '
            f'viewBox="0 0 1024 1024">{STICKER}<g filter="url(#st)">{mascot()}</g></svg>')


def head_only():
    """For the favicon: only the head and the helmet, which read at 32 px."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" '
            f'viewBox="90 60 720 720">{STICKER}<g filter="url(#st)">{head()}{helmet()}</g></svg>')


def touch_icon():
    """iOS fills a transparent touch icon with black, so this one has a light tile."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" '
            f'viewBox="0 0 1024 1024"><rect width="1024" height="1024" fill="#e6efff"/>'
            f'{STICKER}<g transform="translate(-6 0) scale(1.15)" '
            f'filter="url(#st)">{head()}{helmet()}</g></svg>')


def og():
    font = "-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1e40af"/>
<stop offset="1" stop-color="#0d9488"/></linearGradient></defs>{STICKER}
<rect width="1200" height="630" fill="url(#g)"/>
<g font-family="{font}" fill="#ffffff">
<text x="80" y="250" font-size="88" font-weight="800">SpaceWarden</text>
<text x="80" y="326" font-size="44" font-weight="600" fill="#fde68a">Tidy Mac. Zero snooping.</text>
<text x="80" y="402" font-size="29" fill="#e0f2fe">Free up space in a few clicks.</text>
<text x="80" y="442" font-size="29" fill="#e0f2fe">Your files never leave your Mac.</text>
<text x="80" y="540" font-size="23" fill="#bae6fd">Free for macOS 15 and later</text>
</g>
<g transform="translate(630 40) scale(.54)" filter="url(#st)">{mascot()}</g>
</svg>'''


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "touch-icon.svg").write_text(touch_icon())
(OUT / "og.svg").write_text(og())
(OUT / "mascot.svg").write_text(full())
(OUT / "mascot-head.svg").write_text(head_only())
print("wrote", ", ".join(p.name for p in sorted(OUT.glob("*.svg"))))
