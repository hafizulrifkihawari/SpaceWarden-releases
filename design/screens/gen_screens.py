"""Make the marketing screenshots of SpaceWarden.

Each screen copies the real dark-mode UI (layout, strings and colors from the app) with demo
data for a made-up user "alex". No real file name or path goes in. Run:

    python3 -I design/screens/gen_screens.py design/screens/out
    design/screens/render.sh

The text of the cards comes from StorageAdvisor.swift. Keep it in sync when the app changes.
"""
import json
import math
import random
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

# Colors sampled from a dark-mode screenshot of the Debug build (2026-10-18).
CSS = """
:root {
  --win: #27292d; --side: #252528; --card: #2f3034; --card2: #36373b; --btn: #3d3e41;
  --line: #3e3f43; --text: #ececed; --sec: #a6a7a8; --ter: #77787b; --sel: #2d6ed3;
  --cap: #33353a; --link: #4c9bff; --green: #34c759; --orange: #ff9f0a; --blue: #418ff8;
}
* { box-sizing: border-box; }
html, body { margin: 0; background: transparent; }
body {
  font: 13px/1.35 -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
  color: var(--text); -webkit-font-smoothing: antialiased; padding: 60px 90px 120px;
}
.window {
  width: 1120px; height: 720px; border-radius: 12px; overflow: hidden; display: flex;
  background: var(--win); position: relative;
  box-shadow: 0 0 0 0.5px rgba(0,0,0,.9), inset 0 0 0 0.5px rgba(255,255,255,.14),
    0 30px 70px rgba(0,0,0,.45), 0 10px 24px rgba(0,0,0,.3);
}
.sidebar {
  width: 212px; flex: none; background: var(--side); border-right: 1px solid #1c1c1e;
  padding: 10px 8px; position: relative;
}
.lights { display: flex; gap: 8px; padding: 6px 8px 0; height: 32px; }
.lights i { width: 12px; height: 12px; border-radius: 50%; display: block; }
.lights i:nth-child(1) { background: #ff5f57; } .lights i:nth-child(2) { background: #febc2e; }
.lights i:nth-child(3) { background: #28c840; }
.side-toggle { position: absolute; right: 14px; top: 13px; color: var(--sec); }
.group { color: var(--ter); font-size: 11px; font-weight: 600; margin: 14px 8px 4px; }
.item {
  display: flex; align-items: center; gap: 9px; height: 28px; padding: 0 9px;
  border-radius: 7px; font-size: 13px;
}
.item svg { width: 16px; height: 16px; color: var(--blue); flex: none; }
.item.on { background: var(--sel); }
.item.on svg { color: #fff; }
.main { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.toolbar {
  height: 52px; flex: none; display: flex; align-items: center; padding: 0 12px 0 20px;
  gap: 10px;
}
.toolbar h1 { font-size: 15px; font-weight: 700; margin: 0; flex: 1; }
.capsule {
  display: flex; align-items: center; gap: 14px; height: 32px; padding: 0 12px;
  border-radius: 16px; background: var(--cap); color: var(--text); font-size: 13px;
  box-shadow: inset 0 0 0 0.5px rgba(255,255,255,.08);
}
.capsule span { display: flex; align-items: center; gap: 6px; }
.capsule svg { width: 16px; height: 16px; }
.content { flex: 1; overflow: hidden; padding: 4px 20px 20px; }
.box {
  background: var(--card); border-radius: 9px; padding: 12px 14px;
}
.fresh { display: flex; gap: 12px; align-items: flex-start; }
.fresh .ico { color: var(--sec); margin-top: 1px; }
.fresh .ico svg { width: 18px; height: 18px; display: block; }
.fresh b { font-weight: 600; }
.sec { color: var(--sec); }
.ter { color: var(--ter); }
.small { font-size: 11px; }
.btn {
  display: inline-flex; align-items: center; gap: 6px; height: 22px; padding: 0 9px;
  border-radius: 5px; background: var(--btn); color: var(--text); font-size: 13px;
  box-shadow: 0 0.5px 0 rgba(255,255,255,.08) inset, 0 1px 1px rgba(0,0,0,.25);
  white-space: nowrap;
}
.btn svg { width: 14px; height: 14px; }
.btn.primary { background: var(--sel); color: #fff; }
.disclosure { display: flex; align-items: baseline; gap: 6px; font-weight: 700; margin: 18px 0 8px; }
.disclosure svg { width: 10px; height: 10px; color: var(--sec); }
.card {
  display: flex; gap: 12px; padding: 12px; border-radius: 8px;
  background: rgba(255,255,255,.055); margin-bottom: 10px;
}
.card .sym { width: 32px; flex: none; color: var(--blue); display: flex; justify-content: center; }
.card .sym svg { width: 22px; height: 22px; }
.card .body { flex: 1; display: flex; flex-direction: column; gap: 6px; min-width: 0; }
.card .head { display: flex; align-items: baseline; gap: 8px; }
.card .head b { font-weight: 700; }
.card .head .size { margin-left: auto; font-weight: 700; font-variant-numeric: tabular-nums; }
.card .head .x { color: var(--sec); font-size: 12px; margin-left: 8px; }
.badge { font-size: 10px; font-weight: 700; padding: 1px 6px; border-radius: 999px; }
.badge.safe { color: #32d74b; background: rgba(50,215,75,.2); }
.badge.review { color: #ff9f0a; background: rgba(255,159,10,.2); }
.callout { font-size: 12px; color: var(--sec); }
.card .btn { align-self: flex-start; margin-top: 2px; }
.space h3 { margin: 0 0 10px; font-size: 13px; font-weight: 700; }
.bar { display: flex; height: 8px; border-radius: 3px; overflow: hidden; gap: 1px; margin-bottom: 8px; }
.legend { display: flex; justify-content: space-between; gap: 20px; padding: 3px 0; }
.legend .l { display: flex; gap: 8px; }
.legend .dot { width: 7px; height: 7px; border-radius: 50%; margin-top: 5px; flex: none; }
.legend .v { font-variant-numeric: tabular-nums; color: var(--sec); white-space: nowrap; }
.notice { display: flex; align-items: center; gap: 10px; color: var(--sec); margin: 16px 0 0; }
.notice svg { width: 15px; height: 15px; flex: none; }
.map { display: flex; gap: 28px; }
.seg { display: inline-flex; background: var(--cap); border-radius: 6px; padding: 2px; }
.seg span { padding: 2px 10px; border-radius: 5px; }
.seg .on { background: var(--sel); color: #fff; }
.cats { flex: 1; }
.cats h4 { margin: 0; font-size: 13px; font-weight: 700; }
.cat { display: flex; align-items: center; gap: 10px; height: 26px; }
.cat svg.ci { width: 15px; height: 15px; color: var(--sec); flex: none; }
.cat .n { width: 100px; }
.cat .track { flex: 1; height: 8px; }
.cat .track i { display: block; height: 8px; border-radius: 3px; }
.cat .v { width: 76px; text-align: right; font-variant-numeric: tabular-nums; }
.cat .chev { color: var(--ter); font-size: 11px; }
.inspector {
  width: 250px; flex: none; border-left: 1px solid var(--line); background: #252529;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  text-align: center; padding: 20px; color: var(--sec);
}
.vis { display: flex; align-items: center; gap: 16px; padding: 7px 12px; border-bottom: 1px solid var(--line); }
.chk { display: inline-flex; align-items: center; gap: 6px; }
.chk i {
  width: 14px; height: 14px; border-radius: 3.5px; background: #3a3b3f; display: inline-block;
  box-shadow: inset 0 0 0 0.5px rgba(255,255,255,.12);
}
.chk i.on { background: var(--sel); position: relative; }
.chk i.on::after {
  content: ""; position: absolute; left: 4.5px; top: 1.5px; width: 3.5px; height: 7.5px;
  border: solid #fff; border-width: 0 1.8px 1.8px 0; transform: rotate(45deg);
}
.list { padding: 0 12px; }
.ghead {
  display: flex; justify-content: space-between; padding: 12px 6px 5px; font-size: 11px;
  font-weight: 600; color: var(--sec); border-bottom: 1px solid var(--line);
}
.ghead a { color: var(--link); text-decoration: none; }
.frow { display: flex; align-items: center; gap: 10px; padding: 6px; border-bottom: 1px solid rgba(255,255,255,.05); }
.frow .nm { flex: 1; min-width: 0; }
.frow .p { font-size: 11px; color: var(--sec); }
.frow .keep { font-size: 11px; color: #32d74b; }
.frow .d { font-size: 11px; color: var(--sec); width: 76px; text-align: right; }
.footer {
  display: flex; align-items: center; justify-content: space-between; padding: 12px 20px;
  border-top: 1px solid var(--line); font-variant-numeric: tabular-nums;
}
.search {
  display: flex; align-items: center; gap: 6px; width: 170px; height: 28px; padding: 0 9px;
  border-radius: 14px; background: var(--cap); color: var(--ter);
  box-shadow: inset 0 0 0 0.5px rgba(255,255,255,.08);
}
.search svg { width: 13px; height: 13px; }
.tseg { display: inline-flex; background: var(--cap); border-radius: 8px; padding: 2px; height: 28px;
  align-items: center; box-shadow: inset 0 0 0 0.5px rgba(255,255,255,.08); }
.tseg span { display: flex; padding: 3px 9px; border-radius: 6px; color: var(--sec); }
.tseg span svg { width: 15px; height: 15px; }
.tseg .on { background: #5b5c60; color: #fff; }
.kinds { display: flex; background: var(--cap); border-radius: 6px; padding: 2px; margin: 4px 12px 0; }
.kinds span { flex: 1; text-align: center; padding: 2px 0; border-radius: 5px; }
.kinds .on { background: #5b5c60; }
.filters { display: flex; align-items: center; gap: 12px; padding: 8px 12px; font-size: 12px; }
.pop {
  display: inline-flex; align-items: center; gap: 6px; height: 22px; padding: 0 6px 0 8px;
  border-radius: 5px; background: var(--btn); white-space: nowrap;
  box-shadow: 0 0.5px 0 rgba(255,255,255,.08) inset, 0 1px 1px rgba(0,0,0,.25);
}
.pop::after { content: "⌃"; transform: rotate(180deg); font-size: 9px; color: var(--sec); }
.lbl { white-space: nowrap; display: inline-flex; align-items: center; gap: 6px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(152px, 1fr)); gap: 10px; padding: 12px;
  justify-content: start; }
.cell { padding: 6px; border-radius: 8px; text-align: center; }
.cell.on { background: rgba(45,110,211,.25); }
.thumb { width: 128px; height: 128px; margin: 0 auto 4px; display: flex; align-items: center;
  justify-content: center; }
.thumb svg { display: block; border-radius: 2px; box-shadow: 0 1px 3px rgba(0,0,0,.5); }
.cell .n { font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cell .m { font-size: 11px; color: var(--sec); font-variant-numeric: tabular-nums; }
.cell.on .m { color: var(--text); }
.insp { width: 270px; flex: none; border-left: 1px solid var(--line); background: #252529;
  padding: 16px; display: flex; flex-direction: column; gap: 14px; font-size: 12px; }
.insp hr { border: 0; border-top: 1px solid var(--line); margin: 0; width: 100%; }
.insp .hd { display: flex; gap: 12px; align-items: center; }
.insp .hd b { font-size: 13px; }
.kv { display: flex; justify-content: space-between; padding: 2px 0; }
.kv span:first-child { color: var(--sec); }
.ql { height: 300px; border-radius: 6px; background: #1d1e21; display: flex; align-items: center;
  justify-content: center; overflow: hidden; }
.acts { display: flex; flex-wrap: wrap; gap: 8px; }
.arow { display: flex; align-items: baseline; gap: 10px; padding: 9px 4px; margin: 0 8px;
  border-bottom: 1px solid rgba(255,255,255,.07); }
.arow .ai { width: 18px; flex: none; color: var(--blue); position: relative; top: 3px; }
.arow .ai svg { width: 15px; height: 15px; }
.arow.undone .ai { color: var(--sec); }
.arow .tx { flex: 1; min-width: 0; }
.arow .tt { font-size: 13px; font-weight: 700; }
.arow.undone .tt { color: var(--sec); }
.arow .dt { font-size: 11px; color: var(--sec); }
.arow .tm { font-size: 10px; color: var(--ter); margin-top: 1px; }
.arow .disc { width: 10px; color: var(--sec); font-size: 10px; }
"""

ICONS = {
    # Simple outline icons that look like the SF Symbols of the app.
    "overview": '<circle cx="8" cy="8" r="6.3"/><path d="M8 3.6V8l3.2 2.6"/>',
    "explorer": '<path d="M1.8 4.2h4.4l1.4 1.6h6.6v6.6H1.8z"/>',
    "media": '<rect x="1.8" y="3" width="12.4" height="10" rx="1.6"/><circle cx="5.6" cy="6.6" r="1.2"/><path d="M14 11.2 10.6 8 5 13"/>',
    "largeold": '<path d="M3 8a5 5 0 1 0 1.5-3.6M3 2.8v2.4h2.4"/><path d="M8 5.2V8l2 1.4"/>',
    "apps": '<rect x="2.2" y="2.2" width="4.6" height="4.6" rx="1"/><rect x="9.2" y="2.2" width="4.6" height="4.6" rx="1"/><rect x="2.2" y="9.2" width="4.6" height="4.6" rx="1"/><rect x="9.2" y="9.2" width="4.6" height="4.6" rx="1"/>',
    "caches": '<path d="M2.5 4h11M6 4V2.6h4V4M4 4l.7 9.4h6.6L12 4M6.6 6.5v4.6M9.4 6.5v4.6"/>',
    "dupes": '<rect x="5" y="4.6" width="8.4" height="9.4" rx="1.3"/><path d="M3 11.4V3.2A1.2 1.2 0 0 1 4.2 2h6.4"/>',
    "rules": '<rect x="2" y="3" width="12" height="10" rx="1.6"/><path d="M2 7h12M6 10h4"/>',
    "activity": '<path d="M3 8a5 5 0 1 0 1.5-3.6M3 2.8v2.4h2.4"/><path d="M8 5.2V8l2 1.4"/>',
    "clock": '<circle cx="8" cy="8" r="6.3"/><path d="M8 4.4V8l2.4 1.6"/>',
    "scan": '<path d="M13.2 8A5.2 5.2 0 1 1 11.6 4.2M13.2 2.6v3h-3"/>',
    "target": '<circle cx="8" cy="8" r="4.8"/><path d="M8 1.4v3M8 11.6v3M1.4 8h3M11.6 8h3"/>',
    "preview": '<rect x="1.8" y="2.8" width="12.4" height="10.4" rx="1.8"/><path d="M9.6 2.8v10.4M11.4 5.4h1.2M11.4 7.4h1.2"/>',
    "sidebar": '<rect x="1.8" y="2.8" width="12.4" height="10.4" rx="1.8"/><path d="M6.2 2.8v10.4M3.4 5.4h1.2M3.4 7.4h1.2"/>',
    "archivebox": '<rect x="1.8" y="2.6" width="12.4" height="3.2" rx=".8"/><path d="M2.8 5.8v7.6h10.4V5.8M6.4 8.4h3.2"/>',
    "shippingbox": '<path d="M8 1.8 14 4.6v6.8L8 14.2 2 11.4V4.6zM2 4.6l6 2.8 6-2.8M8 7.4v6.8M5 3.2l6 2.8"/>',
    "deps": '<path d="M8 1.8 14 4.6v6.8L8 14.2 2 11.4V4.6zM2 4.6l6 2.8 6-2.8M8 7.4v6.8"/><path d="M5.2 10.2H2.2m1.4-1.4-1.4 1.4 1.4 1.4"/>',
    "hand": '<path d="M5.4 8.4V3.6a.9.9 0 0 1 1.8 0v4M7.2 7.4V2.6a.9.9 0 0 1 1.8 0v4.8M9 7.4V3.4a.9.9 0 0 1 1.8 0v4.8M10.8 8V5.4a.9.9 0 0 1 1.8 0v4.2c0 2.6-1.8 4.6-4.4 4.6-1.6 0-2.6-.7-3.6-2L2.8 9.6a1 1 0 0 1 1.6-1.2L5.4 9.6"/>',
    "chev": '<path d="M3 5.5 8 10.5 13 5.5"/>',
    "dev": '<path d="M2.4 13.6 8.6 7.4M7.4 3.6l5 5M9.6 2.4l4 4-2 2-4-4z"/>',
    "appdata": '<rect x="1.8" y="4" width="12.4" height="9" rx="1.6"/><path d="M1.8 7.4h12.4M5.4 4V2.6h5.2V4"/>',
    "drive": '<rect x="1.8" y="5" width="12.4" height="6.4" rx="1.6"/><path d="M4.4 9.2h1.4"/>',
    "q": '<rect x="2.2" y="2.2" width="11.6" height="11.6" rx="1.6"/><path d="M6.4 6.4a1.6 1.6 0 1 1 2.2 1.5c-.5.2-.6.6-.6 1.1M8 11v.2"/>',
    "doc": '<path d="M4 1.8h5.4l3 3v9.4H4z"/><path d="M9.4 1.8v3h3M6 8.4h4M6 10.6h4"/>',
    "photo": '<rect x="1.8" y="3" width="12.4" height="10" rx="1.6"/><circle cx="5.6" cy="6.6" r="1.2"/><path d="M14 11.2 10.6 8 5 13"/>',
    "app": '<rect x="2.6" y="2.6" width="10.8" height="10.8" rx="2.6"/>',
    "note": '<path d="M6.4 12V3l6-1.2v8.4"/><circle cx="4.8" cy="12" r="1.6"/><circle cx="10.8" cy="10.4" r="1.6"/>',
    "search": '<circle cx="7" cy="7" r="4.6"/><path d="m10.4 10.4 3.4 3.4"/>',
    "list": '<path d="M5.6 4h8M5.6 8h8M5.6 12h8"/><circle cx="2.6" cy="4" r=".5"/><circle cx="2.6" cy="8" r=".5"/><circle cx="2.6" cy="12" r=".5"/>',
    "grid": '<rect x="2.2" y="2.2" width="4.8" height="4.8" rx="1"/><rect x="9" y="2.2" width="4.8" height="4.8" rx="1"/><rect x="2.2" y="9" width="4.8" height="4.8" rx="1"/><rect x="9" y="9" width="4.8" height="4.8" rx="1"/>',
    "trash": '<path d="M2.5 4h11M6 4V2.6h4V4M4 4l.7 9.4h6.6L12 4M6.6 6.5v4.6M9.4 6.5v4.6"/>',
    "movedoc": '<path d="M3 2.4h5l2.4 2.4v3.4M3 2.4v11.2h4.4"/><path d="M9 12h5m-1.8-1.8L14 12l-1.8 1.8"/>',
    "branch": '<path d="M4 14V9.6C4 7.6 5.4 6.4 8 6.4h4M10 4.2l2.2 2.2L10 8.6M4 2v5"/>',
    "film": '<rect x="1.8" y="2.6" width="12.4" height="10.8" rx="1.4"/><path d="M4.8 2.6v10.8M11.2 2.6v10.8M1.8 6h3M1.8 10h3M11.2 6h3M11.2 10h3"/>',
}


def icon(name, cls=""):
    return (f'<svg class="{cls}" viewBox="0 0 16 16" fill="none" stroke="currentColor" '
            f'stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">'
            f'{ICONS[name]}</svg>')


SIDEBAR = [
    ("Storage", [("overview", "Overview"), ("explorer", "Explorer"), ("media", "Media Library"),
                 ("largeold", "Large &amp; Old Files")]),
    ("Clean Up", [("apps", "Applications"), ("caches", "Caches &amp; Junk"),
                  ("dupes", "Duplicates"), ("rules", "Organize Rules"),
                  ("activity", "Activity")]),
]


def sidebar(active):
    rows = ['<div class="lights"><i></i><i></i><i></i></div>',
            f'<div class="side-toggle">{icon("sidebar")}</div>']
    for group, items in SIDEBAR:
        rows.append(f'<div class="group">{group}</div>')
        for key, title in items:
            on = " on" if key == active else ""
            rows.append(f'<div class="item{on}">{icon(key)}{title}</div>')
    return f'<aside class="sidebar">{"".join(rows)}</aside>'


def toolbar(title):
    return f'''<div class="toolbar"><h1>{title}</h1>
<div class="capsule"><span>{icon("target")}Home Folder ⌄</span></div>
<div class="capsule"><span>{icon("preview")}Preview</span><span>{icon("scan")}Full Scan</span>
</div></div>'''


FRESH = f'''<div class="box fresh"><div class="ico">{icon("clock")}</div>
<div style="flex:1"><b>Last full scan: Home Folder, 2 minutes ago</b>
<div class="sec">18 Oct 2026 at 9:41 · 1,204,318 items · 14 s</div>
<div class="sec">The numbers show the disk at that time. They do not update by themselves.
Click Full Scan to read every file again.</div></div>
<span class="btn">{icon("scan")}Full Scan</span></div>'''


def page(body, title):
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>'''


# 1. Overview with recommended actions ---------------------------------------------------

CARDS = [
    ("archivebox", "Remove caches and logs", "safe", "Safe", "9.42 GB",
     "Apps and developer tools keep caches, logs and build results.",
     "Apps make these files again when they need them.", "Open Caches &amp; Junk"),
    ("clock", "Review large old files", "review", "Review", "21.73 GB",
     "7 files of 500 MB or more did not change for 6 months.",
     "Look at each file first. Move the files that you keep to an external disk.",
     "Open Large &amp; Old Files"),
    ("shippingbox", "Remove old installers", "review", "Review", "6.18 GB",
     "14 disk images and installers in Downloads are older than 30 days.",
     "You can download an installer again from its website.", "Open Caches &amp; Junk"),
    ("deps", "Remove dependencies of old projects", "review", "Review", "4.36 GB",
     "23 dependency folders, for example node_modules, are in projects with no change for 3 "
     "months.",
     "Run the install command of the project, for example npm install, to get them back.",
     "Show in Explorer"),
]


def overview(base=False, only=None):
    """base=True: the background of the animated overview, with no cards. It writes the boxes
    of the cards and their close buttons into the page for gen_overview_anim.py.
    only=i: card i alone, on a clear background, as one layer of the animation."""
    cards = []
    for sym, title, cls, badge, size, reason, after, button in CARDS:
        cards.append(f'''<div class="card"><div class="sym">{icon(sym)}</div><div class="body">
<div class="head"><b>{title}</b><span class="badge {cls}">{badge}</span>
<span class="size">{size}</span><span class="x">✕</span></div>
<div>{reason}</div><div class="callout">{after}</div>
<span class="btn">{button}</span></div></div>''')
    content = f'''{FRESH}
<div class="disclosure">{icon("chev")}Recommended Actions</div>
{"".join(cards)}'''
    body = f'''<div class="window">{sidebar("overview")}<div class="main">{toolbar("Overview")}
<div class="content">{content}</div></div></div>'''
    if base:
        body += "<style>.card { visibility: hidden; }</style>" + boxes_script(
            {"cards": ".card", "close": ".card .x"})
    if only is not None:
        body += (f"<style>body {{ visibility: hidden; }} .window {{ box-shadow: none; }}\n"
                 f".card:nth-child({only + 1} of .card) {{ visibility: visible; }}</style>")
    return page(body, "Overview")


def boxes_script(lists):
    """A script that writes the boxes of the elements for each selector into the page."""
    pairs = ",\n".join(
        f'  {name}: [].map.call(document.querySelectorAll("{sel}"), box)'
        for name, sel in lists.items())
    return f'''<pre id="boxes" hidden></pre><script>
function box(el) {{
  var r = el.getBoundingClientRect();
  return {{ x: r.left, y: r.top, w: r.width, h: r.height }};
}}
document.getElementById("boxes").textContent = JSON.stringify({{
{pairs}
}});
</script>'''


# 2. Space and Storage Map ---------------------------------------------------------------

CATS = [  # name, icon, bar color, size in GB
    ("Photos", "photo", "#f47f9b", 48.21), ("Videos", "film", "#c98af5", 36.94),
    ("Developer", "dev", "#7ed783", 31.38), ("App Data", "appdata", "#8b9afc", 22.71),
    ("Documents", "doc", "#6ed7e3", 14.06), ("Caches", "drive", "#f5d854", 11.92),
    ("Audio", "note", "#f9b45a", 7.31), ("Apps", "app", "#5aa6fb", 5.62),
    ("Archives", "archivebox", "#c3a27e", 3.18), ("Other", "q", "#a5a5a7", 1.29),
]
TOTAL = sum(c[3] for c in CATS)


def shade(hex_color, factor):
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v * factor))) for v in (r, g, b))


def arc(cx, cy, r0, r1, a0, a1, fill):
    def pt(r, a):
        t = math.radians(a - 90)
        return cx + r * math.cos(t), cy + r * math.sin(t)
    large = 1 if a1 - a0 > 180 else 0
    x0, y0 = pt(r1, a0); x1, y1 = pt(r1, a1); x2, y2 = pt(r0, a1); x3, y3 = pt(r0, a0)
    return (f'<path d="M{x0:.2f} {y0:.2f}A{r1} {r1} 0 {large} 1 {x1:.2f} {y1:.2f}'
            f'L{x2:.2f} {y2:.2f}A{r0} {r0} 0 {large} 0 {x3:.2f} {y3:.2f}Z" fill="{fill}" '
            f'stroke="#27292d" stroke-width="0.8"/>')


RINGS = [(34, 62), (62, 86), (86, 108), (108, 128), (128, 146)]


def sunburst_segments():
    """Each segment is (category index, depth, start angle, end angle, fill)."""
    rnd = random.Random(7)
    rings = RINGS
    parts = []
    cat = 0

    def split(a0, a1, depth, color):
        if depth >= len(rings) or a1 - a0 < 1.2:
            return
        r0, r1 = rings[depth]
        # Some folders have no deeper level, so the outer rings have gaps.
        if depth >= 3 and rnd.random() < 0.12:
            return
        n = 1 if a1 - a0 < 3 else rnd.randint(2, 6)
        weights = sorted((rnd.random() ** 2 + 0.05 for _ in range(n)), reverse=True)
        fill_share = 1.0 if depth <= 1 else rnd.uniform(0.9, 1.0)
        span = (a1 - a0) * fill_share
        a = a0
        for w in weights:
            b = a + span * w / sum(weights)
            factor = [0.86, 0.76, 0.66, 0.58, 0.52][depth] * rnd.uniform(0.92, 1.06)
            parts.append((cat, depth, a, b, shade(color, factor)))
            split(a, b, depth + 1, color)
            a = b

    a = 0.0
    for cat, (name, _, color, gb) in enumerate(CATS):
        b = a + 360 * gb / TOTAL
        parts.append((cat, 0, a, b, shade(color, 0.86)))
        split(a, b, 1, color)
        a = b
    return parts


def sunburst(size=300):
    c = size / 2
    parts = [arc(c, c, *RINGS[depth], a0, a1, fill)
             for _, depth, a0, a1, fill in sunburst_segments()]
    center = (f'<circle cx="{c}" cy="{c}" r="33" fill="#2a2c2f"/>'
              f'<text x="{c}" y="{c - 9}" fill="#ececed" font-size="11" text-anchor="middle">All'
              f'</text><text x="{c}" y="{c + 6}" fill="#ececed" font-size="11" '
              f'text-anchor="middle">{TOTAL:.2f}</text><text x="{c}" y="{c + 20}" '
              f'fill="#ececed" font-size="11" text-anchor="middle">GB</text>')
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
            f'font-family="-apple-system, sans-serif">{"".join(parts)}{center}</svg>')


def storage_map(base=False):
    """base=True: the background of the animated map. It hides the sunburst and the bars,
    and writes their boxes into the page for gen_storage_anim.py."""
    scanned, outside, purge, free = TOTAL, 41.27, 6.83, 263.66
    disk = scanned + outside + purge + free
    bar = "".join(f'<i style="flex:{v / disk:.4f};background:{col}"></i>' for v, col in [
        (scanned, "#418ff8"), (outside, "#a8a8ac"), (purge, "#6ed7e3"), (free, "#4e7452")])
    legend = [
        ("#418ff8", "Scanned (Home Folder)", "", scanned),
        ("#a8a8ac", "Not in the scan",
         "macOS, apps and other user accounts are outside your Home Folder. 8 folders with "
         "keychains or keys are never scanned. 7 private folders (Mail, Messages and more) were "
         "left out.", outside),
        ("#6ed7e3", "Purgeable", "macOS frees this space when an app needs it.", purge),
        ("#4e7452", "Free", "", free),
    ]
    rows = "".join(
        f'<div class="legend"><div class="l"><i class="dot" style="background:{col}"></i><div>'
        f'{name}{f"<div class=small style=color:var(--sec)>{desc}</div>" if desc else ""}'
        f'</div></div><span class="v">{v:.2f} GB</span></div>' for col, name, desc, v in legend)
    top = max(c[3] for c in CATS)
    cats = "".join(
        f'<div class="cat">{icon(ic, "ci")}<span class="n">{name}</span><span class="track">'
        f'<i style="width:{gb / top * 100:.1f}%;background:{col}"></i></span>'
        f'<span class="v">{gb:.2f} GB</span><span class="chev">›</span></div>'
        for name, ic, col, gb in CATS)
    content = f'''<div class="box space"><h3>Space on Macintosh HD</h3>
<div class="bar">{bar}</div>{rows}</div>
<div class="notice">{icon("hand")}<span>8 folders with keychains or keys are never scanned.
7 private folders (Mail, Messages and more) were not scanned.</span>
<span class="btn" style="color:var(--text)">Privacy Settings</span></div>
<div class="disclosure">{icon("chev")}Storage Map</div>
<div class="map"><div style="width:300px;text-align:center">
<div class="seg"><span class="on">Sunburst</span><span>Treemap</span></div>
<div style="margin-top:6px">{sunburst()}</div></div>
<div class="cats"><h4>By Category</h4>
<div class="sec small" style="margin-bottom:6px">Click a category to see what it holds and
where it is.</div>{cats}</div></div>'''
    body = f'''<div class="window">{sidebar("overview")}<div class="main">{toolbar("Overview")}
<div class="content">{content}</div></div></div>'''
    if base:
        body += BASE_EXTRA
    return page(body, "Storage Map")


BASE_EXTRA = "<style>.map svg, .cat .track i { visibility: hidden; }</style>" + boxes_script(
    {"sunburst": ".map svg", "bars": ".cat .track i", "rows": ".cat"})


def storage_map_data():
    return json.dumps({
        "rings": RINGS,
        "total": round(TOTAL, 2),
        "cats": [{"name": n, "color": col, "gb": gb} for n, _, col, gb in CATS],
        "segments": sunburst_segments(),
    })


# 3. Duplicates --------------------------------------------------------------------------

GROUPS = [
    ("1.42 GB", [("Japan trip 2025.mov", "/Users/alex/Movies", "12 Mar 2025", False),
                 ("Japan trip 2025.mov", "/Users/alex/Downloads", "14 Mar 2025", True)]),
    ("486.2 MB", [("Wedding photos.zip", "/Users/alex/Documents/Family", "2 Jun 2024", False),
                  ("Wedding photos.zip", "/Users/alex/Desktop", "2 Jun 2024", True),
                  ("Wedding photos (1).zip", "/Users/alex/Downloads", "3 Jun 2024", True)]),
    ("212.8 MB", [("Podcast episode 12.wav", "/Users/alex/Music/Podcast", "21 Jan 2025",
                   False),
                  ("Podcast episode 12.wav", "/Users/alex/Desktop/Export", "21 Jan 2025",
                   False)]),
]


def duplicates():
    rows = []
    for size, files in GROUPS:
        rows.append(f'<div class="ghead"><span>{len(files)} copies · {size} each</span>'
                    f'<a>Select Extra Copies</a></div>')
        for i, (name, path, date, picked) in enumerate(files):
            keep = '<span class="keep">Suggested to keep</span>' if i == 0 else ""
            rows.append(f'<div class="frow"><span class="chk"><i class="{"on" if picked else ""}">'
                        f'</i></span><div class="nm"><div>{name}</div><div class="p">{path}</div>'
                        f'</div>{keep}<span class="d">{date}</span></div>')
    content = f'''<div style="padding:4px 20px 0">{FRESH}</div>
<div style="display:flex;align-items:center;padding:10px 20px">
<span class="sec small" style="flex:1">Finds files with the same content in your own folders.
It does not look in ~/Library, app bundles or the Trash.</span>
<span class="btn">{icon("dupes")}Find Duplicates</span></div>
<div class="vis" style="border-top:1px solid var(--line)"><span class="chk"><i></i>Show Hidden
Files</span><span class="chk"><i></i>Show Dependency and Build Folders</span>
<span class="sec" style="margin-left:auto">12 files hidden · 84.2 MB</span></div>
<div class="list" style="flex:1;overflow:hidden">{"".join(rows)}</div>
<div class="footer"><span>Selected: 3 copies, 2.39 GB</span>
<span class="btn primary">Move Selected to Trash…</span></div>'''
    body = f'''<div class="window">{sidebar("dupes")}<div class="main">{toolbar("Duplicates")}
<div style="flex:1;display:flex;flex-direction:column;min-height:0">{content}</div></div></div>'''
    return page(body, "Duplicates")


# 4. Media Library with a preview --------------------------------------------------------

def scene(kind, w, h, uid):
    """A made-up photo: simple shapes in the colors of a landscape. No real picture."""
    g = f"g{uid}"
    skies = {
        "lake": ("#f6b67a", "#9cc3e6"), "beach": ("#7fc4ef", "#d8f0fb"),
        "sunset": ("#3b2c6b", "#f08a4b"), "forest": ("#b7d9ef", "#eaf4f7"),
        "city": ("#0e1736", "#33407a"), "dunes": ("#f3c58e", "#fbe6c4"),
        "snow": ("#6d9fd6", "#dbe9f7"), "flowers": ("#a9d4f2", "#e7f4fb"),
        "portrait": ("#e9d6c3", "#c9a98d"),
    }
    top, bottom = skies[kind]
    shapes = []
    W, H = w, h
    if kind == "lake":
        shapes = [f'<circle cx="{W*.7}" cy="{H*.42}" r="{H*.1}" fill="#ffe2a8"/>',
                  f'<path d="M0 {H*.62}L{W*.22} {H*.32}L{W*.45} {H*.6}L{W*.66} {H*.38}L{W} {H*.62}Z" fill="#4f6b8c"/>',
                  f'<path d="M0 {H*.64}L{W*.3} {H*.46}L{W*.55} {H*.64}Z" fill="#3c5574"/>',
                  f'<rect y="{H*.62}" width="{W}" height="{H*.38}" fill="#6f98c4"/>',
                  f'<rect x="{W*.6}" y="{H*.66}" width="{W*.2}" height="2" fill="#ffe2a8" opacity=".7"/>']
    elif kind == "beach":
        shapes = [f'<rect y="{H*.5}" width="{W}" height="{H*.2}" fill="#2b8fc4"/>',
                  f'<rect y="{H*.56}" width="{W}" height="{H*.1}" fill="#46b3d9"/>',
                  f'<path d="M0 {H*.7}Q{W*.5} {H*.62} {W} {H*.72}V{H}H0Z" fill="#ecd6a8"/>',
                  f'<path d="M{W*.2} {H}C{W*.22} {H*.7} {W*.26} {H*.5} {W*.3} {H*.34}" stroke="#6b4a2c" stroke-width="3" fill="none"/>',
                  f'<path d="M{W*.3} {H*.34}q-{W*.14} 0 -{W*.2} {H*.1}M{W*.3} {H*.34}q{W*.14} -{H*.02} {W*.2} {H*.12}M{W*.3} {H*.34}q-{W*.04} -{H*.12} -{W*.14} -{H*.14}" stroke="#2f7a3b" stroke-width="4" fill="none" stroke-linecap="round"/>']
    elif kind == "sunset":
        shapes = [f'<circle cx="{W*.5}" cy="{H*.62}" r="{H*.17}" fill="#ffcf6b"/>',
                  f'<rect y="{H*.62}" width="{W}" height="{H*.38}" fill="#2a2350"/>',
                  f'<rect x="{W*.36}" y="{H*.68}" width="{W*.28}" height="2" fill="#ffcf6b" opacity=".8"/>',
                  f'<rect x="{W*.42}" y="{H*.75}" width="{W*.16}" height="2" fill="#ffcf6b" opacity=".6"/>']
    elif kind == "forest":
        trees = "".join(
            f'<path d="M{x} {H*.9}L{x+W*.07} {H*(.38+.08*(i%3))}L{x+W*.14} {H*.9}Z" fill="{c}"/>'
            for i, (x, c) in enumerate((W*f, c) for f, c in [
                (-.04, "#2f6b45"), (.1, "#245a3a"), (.25, "#3a7d50"), (.4, "#2a6340"),
                (.55, "#336f48"), (.7, "#245a3a"), (.85, "#3a7d50")]))
        shapes = [f'<rect y="{H*.6}" width="{W}" height="{H*.4}" fill="#5f8f5a"/>', trees]
    elif kind == "city":
        rnd = random.Random(3)
        x, bl = 0.0, []
        while x < W:
            bw = rnd.uniform(W*.07, W*.14); bh = rnd.uniform(H*.25, H*.6)
            bl.append(f'<rect x="{x:.1f}" y="{H-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="#1a2140"/>')
            for _ in range(int(bh/7)):
                if rnd.random() < .55:
                    bl.append(f'<rect x="{x+rnd.uniform(2,bw-4):.1f}" y="{H-rnd.uniform(4,bh-4):.1f}" width="2" height="2" fill="#ffd27a"/>')
            x += bw + 1
        shapes = [f'<circle cx="{W*.8}" cy="{H*.2}" r="{H*.06}" fill="#e8ecf7"/>'] + bl
    elif kind == "dunes":
        shapes = [f'<circle cx="{W*.25}" cy="{H*.3}" r="{H*.09}" fill="#fff4dc"/>',
                  f'<path d="M0 {H*.62}Q{W*.3} {H*.42} {W*.6} {H*.6}T{W} {H*.55}V{H}H0Z" fill="#e2a15f"/>',
                  f'<path d="M0 {H*.8}Q{W*.4} {H*.6} {W} {H*.78}V{H}H0Z" fill="#c9824a"/>']
    elif kind == "snow":
        shapes = [f'<path d="M0 {H*.75}L{W*.35} {H*.22}L{W*.6} {H*.55}L{W*.75} {H*.38}L{W} {H*.72}V{H}H0Z" fill="#7a8fa8"/>',
                  f'<path d="M{W*.27} {H*.34}L{W*.35} {H*.22}L{W*.43} {H*.34}L{W*.38} {H*.31}L{W*.33} {H*.36}Z" fill="#fff"/>',
                  f'<path d="M0 {H*.82}Q{W*.5} {H*.7} {W} {H*.84}V{H}H0Z" fill="#f2f6fb"/>']
    elif kind == "flowers":
        rnd = random.Random(5)
        fl = "".join(f'<circle cx="{rnd.uniform(0,W):.1f}" cy="{rnd.uniform(H*.6,H):.1f}" r="{rnd.uniform(1.5,3.2):.1f}" fill="{rnd.choice(["#ff6b8b","#ffd23f","#ffffff","#c77dff"])}"/>' for _ in range(60))
        shapes = [f'<path d="M0 {H*.55}Q{W*.5} {H*.45} {W} {H*.55}V{H}H0Z" fill="#6aa84f"/>', fl]
    elif kind == "portrait":
        shapes = [f'<circle cx="{W*.5}" cy="{H*.4}" r="{W*.17}" fill="#8a6a55"/>',
                  f'<path d="M{W*.12} {H}Q{W*.5} {H*.52} {W*.88} {H}Z" fill="#3f5c7a"/>',
                  f'<path d="M{W*.33} {H*.36}Q{W*.5} {H*.12} {W*.67} {H*.36}Q{W*.5} {H*.26} {W*.33} {H*.36}Z" fill="#3a2a22"/>']
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><linearGradient id="{g}" '
            f'x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" '
            f'stop-color="{bottom}"/></linearGradient></defs><rect width="{W}" height="{H}" '
            f'fill="url(#{g})"/>{"".join(shapes)}</svg>')


PHOTOS = [  # name, scene, landscape?, size, last opened
    ("Lake Bled sunrise.jpg", "lake", True, "18.4 MB", "Aug 2024"),
    ("Bali beach.heic", "beach", True, "6.2 MB", "Jul 2023"),
    ("Lisbon sunset.jpg", "sunset", True, "12.9 MB", "May 2024"),
    ("Black Forest walk.jpg", "forest", False, "9.7 MB", "Sep 2022"),
    ("Tokyo at night.heic", "city", True, "7.8 MB", "Mar 2025"),
    ("Sahara dunes.jpg", "dunes", True, "15.1 MB", "Nov 2022"),
    ("Alps ski trip.jpg", "snow", True, "11.3 MB", "Feb 2023"),
    ("Spring garden.heic", "flowers", False, "5.4 MB", "Apr 2025"),
    ("Grandma 80th.jpg", "portrait", False, "8.6 MB", "Dec 2024"),
]


def thumb(kind, landscape, uid, side=128):
    w, h = (side, round(side * .667)) if landscape else (round(side * .75), side)
    return scene(kind, w, h, uid)


def media_library():
    cells = []
    for i, (name, kind, land, size, used) in enumerate(PHOTOS):
        on = " on" if i == 0 else ""
        cells.append(f'<div class="cell{on}"><div class="thumb">{thumb(kind, land, i)}</div>'
                     f'<div class="n">{name}</div><div class="m">{size} · {used}</div></div>')
    toolbar_html = f'''<div class="toolbar"><h1>Media Library</h1>
<div class="capsule"><span>{icon("target")}Home Folder ⌄</span></div>
<div class="search">{icon("search")}Filter by Name</div>
<div class="tseg"><span>{icon("list")}</span><span class="on">{icon("grid")}</span></div>
<div class="capsule"><span>{icon("trash")}Move 1 to Trash · 18.4 MB</span></div>
<div class="capsule"><span>{icon("preview")}Preview</span></div></div>'''
    kinds = "".join(f'<span class="{"on" if k == "Pictures" else ""}">{k} ({n})</span>' for k, n in [
        ("Pictures", "2,418"), ("Videos", "164"), ("Audio", "392"), ("Documents", "1,807")])
    main = f'''<div style="padding:4px 12px 4px">{FRESH}</div>
<div class="kinds">{kinds}</div>
<div class="filters"><span class="pop">All Locations</span>
<span class="lbl">Larger than <span class="pop">Any size</span></span>
<span class="lbl">Sort <span class="pop">Largest First</span></span>
<span class="sec" style="margin-left:auto;white-space:nowrap">2,418 files · 21.64 GB</span></div>
<div class="vis" style="border-top:1px solid var(--line)"><span class="chk"><i class="on"></i>Show
Hidden Files</span><span class="chk"><i class="on"></i>Show Dependency and Build Folders</span></div>
<div class="grid">{"".join(cells)}</div>'''
    big = scene("lake", 238, 159, "big")
    insp = f'''<div class="insp"><div class="hd">{thumb("lake", True, "hd", 48)}
<div><b>Lake Bled sunrise.jpg</b><div class="sec">18.4 MB</div></div></div>
<div><div class="kv"><span>Kind</span><span>JPEG image</span></div>
<div class="kv"><span>Category</span><span>Photos</span></div>
<div class="kv"><span>Modified</span><span>14 Aug 2024 at 06:12</span></div>
<div class="kv"><span>Last opened</span><span>21 Aug 2024</span></div>
<div class="sec small" style="margin-top:6px">/Users/alex/Pictures/Slovenia 2024/Lake Bled
sunrise.jpg</div></div><hr>
<div class="ql">{big}</div><hr>
<div class="acts"><span class="btn">Reveal in Finder</span><span class="btn">Show in Explorer</span>
<span class="btn">Open</span></div></div>'''
    body = f'''<div class="window">{sidebar("media")}<div class="main">{toolbar_html}
<div style="display:flex;flex:1;min-height:0;border-top:1px solid #1c1c1e">
<div style="flex:1;min-width:0;display:flex;flex-direction:column;overflow:hidden">{main}</div>
{insp}</div></div></div>'''
    return page(body, "Media Library")


# 5. Activity ----------------------------------------------------------------------------

ACTIVITY = [  # icon, title, detail, time, undone
    ("branch", "Organize Rules run: 38 moves", "Click the arrow to see each move.",
     "18 Oct 2026 at 9:52", False),
    ("trash", "Moved to Trash", "/Users/alex/Downloads/Xcode_16.4.xip", "18 Oct 2026 at 9:47",
     False),
    ("trash", "Moved to Trash", "/Users/alex/Downloads/Figma-Installer.dmg",
     "18 Oct 2026 at 9:47", False),
    ("trash", "Moved to Trash", "/Users/alex/Movies/Japan trip 2025 (copy).mov",
     "18 Oct 2026 at 9:45", False),
    ("movedoc", "Renamed", "/Users/alex/Documents/Scan 0012.pdf → "
     "/Users/alex/Documents/Lease agreement 2026.pdf", "18 Oct 2026 at 9:44", False),
    ("trash", "Moved to Trash (undone)", "/Users/alex/Pictures/Slovenia 2024/Lake Bled "
     "sunrise.jpg", "18 Oct 2026 at 9:43", True),
    ("movedoc", "Moved", "/Users/alex/Desktop/Tax receipts 2025 → "
     "/Users/alex/Documents/Finance/Tax receipts 2025", "18 Oct 2026 at 9:40", False),
    ("trash", "Moved to Trash", "/Users/alex/Library/Caches/com.spotify.client",
     "18 Oct 2026 at 9:38", False),
    ("trash", "Moved to Trash", "/Users/alex/Projects/old-portfolio/node_modules",
     "18 Oct 2026 at 9:38", False),
    ("trash", "Moved to Trash", "/Users/alex/Downloads/Zoom.pkg", "17 Oct 2026 at 18:21",
     False),
]


def activity():
    rows = []
    for i, (ic, title, detail, when, undone) in enumerate(ACTIVITY):
        cls = " undone" if undone else ""
        disc = '<span class="disc">›</span>' if ic == "branch" else ""
        btn = "" if undone else ('<span class="btn">Undo Run</span>' if ic == "branch"
                                 else '<span class="btn">Undo</span>')
        rows.append(f'<div class="arow{cls}">{disc}<span class="ai">{icon(ic)}</span>'
                    f'<div class="tx"><div class="tt">{title}</div><div class="dt">{detail}</div>'
                    f'<div class="tm">{when}</div></div>{btn}</div>')
    main = f'''<div style="display:flex;align-items:center;padding:10px 20px">
<span class="sec" style="flex:1;white-space:nowrap">SpaceWarden records every move, rename and move to the Trash. You
can undo each one.</span><span class="btn">Clear History</span></div>
<div style="border-top:1px solid var(--line);padding-top:4px">{"".join(rows)}</div>'''
    insp = f'''<div class="inspector" style="width:220px">{icon("preview").replace("<svg ", '<svg style="width:46px;height:46px;stroke-width:1" ', 1)}
<div style="font-size:22px;font-weight:700;color:var(--sec);margin:12px 0 6px">No Selection</div>
<div>Select a file or a folder to see its details and a preview.</div></div>'''
    body = f'''<div class="window">{sidebar("activity")}<div class="main">{toolbar("Activity")}
<div style="display:flex;flex:1;min-height:0">
<div style="flex:1;min-width:0;overflow:hidden">{main}</div>{insp}</div></div></div>'''
    return page(body, "Activity")


(OUT / "overview.html").write_text(overview())
(OUT / "overview-base.html").write_text(overview(base=True))
for i in range(len(CARDS)):
    (OUT / f"overview-card{i + 1}.html").write_text(overview(only=i))
(OUT / "storage-map.html").write_text(storage_map())
(OUT / "storage-map-base.html").write_text(storage_map(base=True))
(OUT / "storage-map.json").write_text(storage_map_data())
(OUT / "duplicates.html").write_text(duplicates())
(OUT / "media-library.html").write_text(media_library())
(OUT / "activity.html").write_text(activity())
print("wrote", ", ".join(p.name for p in sorted(OUT.glob("*.html"))))
