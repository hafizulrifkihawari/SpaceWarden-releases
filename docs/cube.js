/* SpaceWarden landing page cube.

   On large screens, the sections become the six sides of a cube. The visitor turns the cube
   by drag, scroll wheel, arrow keys or the tabs under it. "Unfold" unfolds the cube into a flat
   net and grows one side to show all of its content. "How it works" shows a guide to the
   controls. On small screens, with reduced motion,
   or without this script, the page stays a normal scroll page. No libraries. */

(function () {
  "use strict";

  // These durations match the transitions in style.css.
  var FOLD_MS = 700;
  var OPEN_MS = 550;
  var TURN_MS = 520;
  var ROLL_MS = 320;
  var BASE_SIDE = 740;
  var DEG_PER_PX = 0.22;
  var MAX_TILT = 5;

  // The light comes from the top left, in front of the cube. A side that faces the viewer
  // has no shade. A side turned away from the light gets up to MAX_SHADE.
  var LIGHT = [-0.35, -0.6, 0.72];
  var FULL_LIGHT = 0.72;
  var MAX_SHADE = 0.2;

  var ORDER = ["front", "right", "back", "left", "bottom", "top"];

  // Each arrow key turns the cube 90 degrees about a screen axis. The side next to the
  // current side, in the direction of the arrow, comes to the front.
  var ARROWS = {
    ArrowRight: axisAngle(0, 1, 0, -90),
    ArrowLeft: axisAngle(0, 1, 0, 90),
    ArrowDown: axisAngle(1, 0, 0, 90),
    ArrowUp: axisAngle(1, 0, 0, -90),
  };

  // In the net, an arrow key opens the next side in that direction, as on the upright cube.
  var NET_MOVES = {
    front: { ArrowLeft: "left", ArrowRight: "right", ArrowUp: "top", ArrowDown: "bottom" },
    right: { ArrowLeft: "front", ArrowRight: "back", ArrowUp: "top", ArrowDown: "bottom" },
    back: { ArrowLeft: "right", ArrowRight: "left", ArrowUp: "top", ArrowDown: "bottom" },
    left: { ArrowLeft: "back", ArrowRight: "front", ArrowUp: "top", ArrowDown: "bottom" },
    top: { ArrowLeft: "left", ArrowRight: "right", ArrowUp: "back", ArrowDown: "front" },
    bottom: { ArrowLeft: "left", ArrowRight: "right", ArrowUp: "front", ArrowDown: "back" },
  };

  // For each side: its outward normal, the rotation that brings it to the front, upright,
  // and its cell in the net (in sides, from the front cell).
  var SIDES = {
    front: { normal: [0, 0, 1], q: axisAngle(0, 1, 0, 0), cell: [0, 0] },
    right: { normal: [1, 0, 0], q: axisAngle(0, 1, 0, -90), cell: [1, 0] },
    back: { normal: [0, 0, -1], q: axisAngle(0, 1, 0, 180), cell: [2, 0] },
    left: { normal: [-1, 0, 0], q: axisAngle(0, 1, 0, 90), cell: [-1, 0] },
    top: { normal: [0, -1, 0], q: axisAngle(1, 0, 0, -90), cell: [0, -1] },
    bottom: { normal: [0, 1, 0], q: axisAngle(1, 0, 0, 90), cell: [0, 1] },
  };

  // Quaternions are [w, x, y, z], in CSS coordinates (x right, y down, z to the viewer).

  function axisAngle(x, y, z, deg) {
    var len = Math.hypot(x, y, z) || 1;
    var half = (deg * Math.PI) / 360;
    var s = Math.sin(half) / len;
    return [Math.cos(half), x * s, y * s, z * s];
  }

  function mul(a, b) {
    return [
      a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3],
      a[0] * b[1] + a[1] * b[0] + a[2] * b[3] - a[3] * b[2],
      a[0] * b[2] - a[1] * b[3] + a[2] * b[0] + a[3] * b[1],
      a[0] * b[3] + a[1] * b[2] - a[2] * b[1] + a[3] * b[0],
    ];
  }

  function normalize(q) {
    var len = Math.hypot(q[0], q[1], q[2], q[3]) || 1;
    return [q[0] / len, q[1] / len, q[2] / len, q[3] / len];
  }

  function rotate(q, v) {
    var p = mul(mul(q, [0, v[0], v[1], v[2]]), [q[0], -q[1], -q[2], -q[3]]);
    return [p[1], p[2], p[3]];
  }

  function dot(a, b) {
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3];
  }

  function slerp(a, b, t) {
    var d = dot(a, b);
    if (d < 0) {
      b = [-b[0], -b[1], -b[2], -b[3]];
      d = -d;
    }
    if (d > 0.9995) {
      return normalize([
        a[0] + (b[0] - a[0]) * t,
        a[1] + (b[1] - a[1]) * t,
        a[2] + (b[2] - a[2]) * t,
        a[3] + (b[3] - a[3]) * t,
      ]);
    }
    var theta = Math.acos(d);
    var sa = Math.sin((1 - t) * theta) / Math.sin(theta);
    var sb = Math.sin(t * theta) / Math.sin(theta);
    return [
      a[0] * sa + b[0] * sb,
      a[1] * sa + b[1] * sb,
      a[2] * sa + b[2] * sb,
      a[3] * sa + b[3] * sb,
    ];
  }

  function toCss(q) {
    var w = Math.max(-1, Math.min(1, q[0]));
    var s = Math.sqrt(1 - w * w);
    if (s < 1e-6) {
      return "rotate3d(0, 1, 0, 0deg)";
    }
    var deg = (2 * Math.acos(w) * 180) / Math.PI;
    return "rotate3d(" + q[1] / s + ", " + q[2] / s + ", " + q[3] / s + ", " + deg + "deg)";
  }

  // The side that faces the viewer most.
  function facing(q) {
    var best = "front";
    var bestZ = -2;
    ORDER.forEach(function (name) {
      var z = rotate(q, SIDES[name].normal)[2];
      if (z > bestZ) {
        bestZ = z;
        best = name;
      }
    });
    return best;
  }

  function ease(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  function wait(ms) {
    return new Promise(function (resolve) {
      setTimeout(resolve, ms);
    });
  }

  var root = document.documentElement;
  var stage = document.querySelector(".cube-stage");
  var supported =
    "inert" in HTMLElement.prototype &&
    window.CSS &&
    CSS.supports("width: calc(1px * sin(1deg))");
  if (!stage || !supported) {
    return;
  }
  var scaler = stage.querySelector(".cube-scaler");
  var cube = stage.querySelector(".cube");
  var media = window.matchMedia(
    "(min-width: 900px) and (min-height: 640px) and (prefers-reduced-motion: no-preference)"
  );

  var faces = {};
  var idToSide = {};
  cube.querySelectorAll(".face").forEach(function (face) {
    var name = face.dataset.face;
    faces[name] = face;
    face.querySelectorAll("[id]").forEach(function (el) {
      idToSide[el.id] = name;
    });
  });

  var q = SIDES.front.q;
  var current = "front";
  var openSide = null;
  // idle, drag, turn, fold (an open or close is running) or open.
  var mode = "idle";
  var active = false;
  // Each enable and disable starts a new run. Async steps of an older run stop.
  var run = 0;
  var turnFrame = 0;
  // Resolves the running turn with false when a new turn replaces it.
  var endTurn = null;
  var tilt = [0, 0];
  var tiltTarget = [0, 0];
  var tiltFrame = 0;
  var drag = null;
  var suppressClick = false;
  var wheelSum = 0;
  var wheelLock = false;
  // Arrow keys pressed during a turn. They run in order when the turn ends.
  var keyQueue = [];
  var MAX_QUEUE = 3;

  // Controls under the cube, and the Open button on each side. The script makes them, so the
  // page without the script has no buttons that do nothing.
  var ui = document.createElement("div");
  ui.className = "cube-ui";
  var tabs = document.createElement("div");
  tabs.className = "cube-tabs";
  tabs.setAttribute("role", "group");
  tabs.setAttribute("aria-label", "Sides of the cube");
  var tabButtons = {};
  ORDER.forEach(function (name) {
    var button = document.createElement("button");
    button.type = "button";
    button.textContent = faces[name].dataset.label;
    button.addEventListener("click", function () {
      if (mode === "open") {
        switchOpen(name);
      } else if (mode === "idle" || mode === "turn") {
        turnTo(name);
      }
    });
    tabButtons[name] = button;
    tabs.appendChild(button);
  });
  var help = document.createElement("div");
  help.className = "cube-help";
  var hint = document.createElement("span");
  var toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "cube-toggle";
  toggle.addEventListener("click", function () {
    if (mode === "open") {
      close();
    } else {
      open(current);
    }
  });
  var guideButton = document.createElement("button");
  guideButton.type = "button";
  guideButton.className = "cube-guide-open";
  guideButton.setAttribute("aria-haspopup", "dialog");
  guideButton.innerHTML =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" ' +
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6v.6' +
    'M12 17h.01"/></svg>How it works';
  guideButton.addEventListener("click", showGuide);
  help.append(hint, toggle, guideButton);
  var live = document.createElement("p");
  live.className = "visually-hidden";
  live.setAttribute("aria-live", "polite");
  ui.append(tabs, help, live);
  stage.appendChild(ui);

  ORDER.forEach(function (name) {
    var button = document.createElement("button");
    button.type = "button";
    button.className = "btn face-open";
    button.innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
      'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>Unfold this side';
    button.addEventListener("click", function () {
      open(name);
    });
    faces[name].appendChild(button);
  });

  // The guide explains the controls. Its map shows the sides as the net shows them. A click
  // on a side in the map goes to that side.
  var guide = document.createElement("dialog");
  guide.className = "cube-guide";
  guide.setAttribute("aria-labelledby", "cube-guide-title");
  guide.innerHTML =
    '<button type="button" class="preview-close" aria-label="Close the guide">&times;</button>' +
    '<h2 id="cube-guide-title">How the cube works</h2>' +
    "<p>Each side of the cube is one part of this page. Home is in the middle. The cube " +
    "unfolds into this map.</p>" +
    '<div class="guide-map" role="group" aria-label="Map of the sides"></div>' +
    '<div class="guide-steps">' +
    "<section><h3>Turn the cube</h3><ul>" +
    "<li>Drag the cube.</li>" +
    "<li>Scroll with the mouse or the trackpad.</li>" +
    "<li>Press an arrow key. The side in that direction comes to the front.</li>" +
    "<li>Click a name in the bar under the cube.</li>" +
    "</ul></section>" +
    "<section><h3>Unfold a side</h3><ul>" +
    "<li>Press <kbd>Enter</kbd>.</li>" +
    "<li>Click <b>Unfold</b> or <b>Unfold this side</b>.</li>" +
    "<li>The side grows, so you can read all of it.</li>" +
    "</ul></section>" +
    "<section><h3>When it is unfolded</h3><ul>" +
    "<li>Press an arrow key to go to the next side.</li>" +
    "<li>On a long side, <kbd>↑</kbd> and <kbd>↓</kbd> scroll first.</li>" +
    "<li>Press <kbd>Esc</kbd>, click <b>Fold back</b> or click outside the side to " +
    "fold it back.</li>" +
    "</ul></section>" +
    "</div>" +
    '<p class="guide-foot">Press <kbd>?</kbd> to show this guide again.</p>';
  var guideMap = guide.querySelector(".guide-map");
  var guideCells = {};
  ORDER.forEach(function (name) {
    var cell = document.createElement("button");
    cell.type = "button";
    cell.textContent = faces[name].dataset.label;
    cell.style.gridColumn = SIDES[name].cell[0] + 2;
    cell.style.gridRow = SIDES[name].cell[1] + 2;
    cell.addEventListener("click", function () {
      guide.close();
      if (mode === "open") {
        switchOpen(name);
      } else if (mode === "idle" || mode === "turn") {
        turnTo(name);
      }
    });
    guideCells[name] = cell;
    guideMap.appendChild(cell);
  });
  guide.querySelector(".preview-close").addEventListener("click", function () {
    guide.close();
  });
  // A click on the backdrop has the dialog itself as its target.
  guide.addEventListener("click", function (e) {
    if (e.target === guide) guide.close();
  });

  function showGuide() {
    var here = mode === "open" ? openSide : current;
    ORDER.forEach(function (name) {
      guideCells[name].setAttribute("aria-current", name === here ? "true" : "false");
    });
    if (!guide.isConnected) document.body.appendChild(guide);
    guide.showModal();
  }

  function render() {
    var tiltX = "rotateX(" + tilt[0].toFixed(3) + "deg) ";
    var tiltY = "rotateY(" + tilt[1].toFixed(3) + "deg) ";
    stage.style.setProperty("--rot", tiltX + tiltY + toCss(q));
    ORDER.forEach(function (name) {
      var n = rotate(q, SIDES[name].normal);
      var lit = n[0] * LIGHT[0] + n[1] * LIGHT[1] + n[2] * LIGHT[2];
      var shade = Math.min(1, Math.max(0, (FULL_LIGHT - lit) / FULL_LIGHT));
      faces[name].style.setProperty("--shade", (shade * MAX_SHADE).toFixed(3));
    });
  }

  function size() {
    var w = stage.clientWidth;
    var h = stage.clientHeight;
    var controls = parseFloat(getComputedStyle(stage).getPropertyValue("--ui")) || 112;
    return { w: w, h: h, avail: h - controls };
  }

  function layout() {
    var box = size();
    var s = Math.floor(Math.min(box.w - 96, box.avail - 32));
    stage.style.setProperty("--s", s + "px");
    // The side content is laid out for a 740 px side. Larger sides zoom it up to fill them.
    stage.style.setProperty("--zoom", Math.max(1, s / BASE_SIDE).toFixed(3));
    if (mode === "open") {
      setOpenBox(faces[openSide]);
      scaler.style.transform = cellTransform(openSide);
    }
    measure();
  }

  function side() {
    return parseFloat(stage.style.getPropertyValue("--s"));
  }

  // The scaler transform that shows the whole net.
  function netTransform() {
    var s = side();
    var box = size();
    var scale = Math.min((box.w - 48) / (4 * s), (box.avail - 24) / (3 * s), 1);
    // The net is 4 sides wide. Its center is half a side to the right of the front side.
    return "translate(" + (-scale * s) / 2 + "px, 0px) scale(" + scale + ")";
  }

  // The scaler transform that centers one cell of the net at full size.
  function cellTransform(name) {
    var s = side();
    var cell = SIDES[name].cell;
    return "translate(" + -cell[0] * s + "px, " + -cell[1] * s + "px) scale(1)";
  }

  function setOpenBox(face) {
    var s = side();
    var box = size();
    var cell = SIDES[face.dataset.face].cell;
    var w = Math.max(s, Math.min(box.w - 64, 1400));
    var h = box.avail - 24;
    face.style.setProperty("--ow", w + "px");
    face.style.setProperty("--oh", h + "px");
    face.style.setProperty("--ox", s / 2 + cell[0] * s - w / 2 + "px");
    face.style.setProperty("--oy", s / 2 + cell[1] * s - h / 2 + "px");
  }

  function measure() {
    ORDER.forEach(function (name) {
      var face = faces[name];
      if (!face.classList.contains("is-open")) {
        face.classList.toggle("is-overflowing", face.scrollHeight > face.clientHeight + 4);
        // A side with hidden extra content, such as more screenshots, also gets the button.
        face.classList.toggle("has-more", !!face.querySelector(".face-extra"));
      }
    });
  }

  function setInert(only) {
    ORDER.forEach(function (name) {
      faces[name].inert = name !== only;
    });
  }

  function setHash(name) {
    var id = name === "front" ? "" : faces[name].querySelector("section").id;
    var url = location.pathname + location.search + (id ? "#" + id : "");
    history.replaceState(null, "", url);
  }

  function setCurrent(name) {
    current = name;
    setInert(name);
    ORDER.forEach(function (other) {
      tabButtons[other].setAttribute("aria-current", other === name ? "true" : "false");
    });
    live.textContent = "Showing: " + faces[name].dataset.label;
    setHash(name);
  }

  function setHelp() {
    if (mode === "open") {
      hint.textContent = "Use the arrow keys to go to the next side. Press Escape to fold it back.";
      toggle.innerHTML =
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" ' +
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M4 14h6v6M20 10h-6V4M14 10l7-7M10 14l-7 7"/></svg>Fold back';
      toggle.classList.add("is-fold");
    } else {
      hint.textContent = "Drag, scroll or use the arrow keys to turn. Press Enter to unfold.";
      toggle.textContent = "Unfold";
      toggle.classList.remove("is-fold");
    }
  }

  function stopTurn() {
    cancelAnimationFrame(turnFrame);
    if (endTurn) {
      endTurn(false);
      endTurn = null;
    }
  }

  // Turns the cube to the rotation "to". Resolves true when it gets there.
  function slerpTo(to, ms) {
    stopTurn();
    var from = q;
    var start = performance.now();
    return new Promise(function (resolve) {
      endTurn = resolve;
      function step(now) {
        if (!active) {
          endTurn = null;
          resolve(false);
          return;
        }
        var t = Math.min(1, (now - start) / ms);
        q = slerp(from, to, ease(t));
        render();
        if (t < 1) {
          turnFrame = requestAnimationFrame(step);
        } else {
          q = to;
          endTurn = null;
          resolve(true);
        }
      }
      turnFrame = requestAnimationFrame(step);
    });
  }

  function turnTo(name, ms) {
    var token = run;
    mode = "turn";
    setCurrent(name);
    return slerpTo(SIDES[name].q, ms || TURN_MS).then(function (done) {
      if (done && token === run && mode === "turn") {
        mode = "idle";
        runPendingKey();
      }
    });
  }

  // Turns 90 degrees in the direction of the arrow first, then rolls the new side upright if
  // it is not. A direct turn to the upright side can tumble on a diagonal instead.
  async function arrowTurn(key) {
    var token = run;
    var turned = mul(ARROWS[key], SIDES[current].q);
    var name = facing(turned);
    mode = "turn";
    setCurrent(name);
    var done = await slerpTo(turned, TURN_MS);
    if (done && Math.abs(dot(turned, SIDES[name].q)) < 0.9999) {
      done = await slerpTo(SIDES[name].q, ROLL_MS);
    }
    if (done && token === run && mode === "turn") {
      mode = "idle";
      runPendingKey();
    }
  }

  function runPendingKey() {
    if (keyQueue.length) {
      arrowTurn(keyQueue.shift());
    }
  }

  function focusHeading(face) {
    var heading = face.querySelector("h1, h2");
    if (heading) {
      heading.tabIndex = -1;
      heading.focus({ preventScroll: true });
    }
  }

  async function open(name) {
    if (mode !== "idle" && mode !== "turn") {
      return;
    }
    var token = run;
    mode = "fold";
    tiltTarget = [0, 0];
    tilt = [0, 0];
    // The net unfolds around the front side, so turn the cube to the front first.
    if (dot(q, SIDES.front.q) < 0.9999) {
      await slerpTo(SIDES.front.q, TURN_MS);
      if (token !== run) return;
    }
    stage.classList.add("is-net");
    scaler.style.transform = netTransform();
    await wait(FOLD_MS);
    if (token !== run) return;
    stage.classList.add("is-flat");
    var face = faces[name];
    face.scrollTop = 0;
    setOpenBox(face);
    // Let the flat state apply before the side grows.
    await wait(30);
    if (token !== run) return;
    face.classList.add("is-open");
    stage.classList.add("is-reading");
    scaler.style.transform = cellTransform(name);
    await wait(OPEN_MS);
    if (token !== run) return;
    openSide = name;
    mode = "open";
    setCurrent(name);
    live.textContent = "Opened: " + face.dataset.label;
    setHelp();
    focusHeading(face);
  }

  async function switchOpen(name) {
    if (mode !== "open" || name === openSide) {
      return;
    }
    var token = run;
    mode = "fold";
    var old = faces[openSide];
    var face = faces[name];
    old.classList.remove("is-open");
    old.scrollTop = 0;
    face.scrollTop = 0;
    setOpenBox(face);
    face.classList.add("is-open");
    scaler.style.transform = cellTransform(name);
    await wait(OPEN_MS);
    if (token !== run) return;
    openSide = name;
    mode = "open";
    setCurrent(name);
    live.textContent = "Opened: " + face.dataset.label;
    focusHeading(face);
  }

  async function close() {
    if (mode !== "open") {
      return;
    }
    var token = run;
    var name = openSide;
    var face = faces[name];
    var hadFocus = face.contains(document.activeElement);
    mode = "fold";
    face.classList.remove("is-open");
    stage.classList.remove("is-reading");
    face.scrollTop = 0;
    scaler.style.transform = netTransform();
    await wait(OPEN_MS);
    if (token !== run) return;
    stage.classList.remove("is-flat");
    stage.classList.remove("is-net");
    scaler.style.transform = "";
    await wait(FOLD_MS);
    if (token !== run) return;
    openSide = null;
    measure();
    setHelp();
    await turnTo(name, 650);
    if (hadFocus) {
      stage.focus({ preventScroll: true });
    }
  }

  // A section under another section on its side, such as Install under Home. The closed
  // side does not show it, so the side must open.
  function isLower(id) {
    var target = document.getElementById(id);
    var face = faces[idToSide[id]];
    return target.parentElement === face && target !== face.firstElementChild;
  }

  // Goes to the side that holds the element with this id.
  function go(id) {
    var name = idToSide[id];
    var target = document.getElementById(id);
    var show = function () {
      if (target.closest(".face") === faces[openSide]) {
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    };
    if (mode === "open") {
      if (name === openSide) {
        show();
      } else {
        switchOpen(name).then(show);
      }
    } else if (mode === "idle" || mode === "turn") {
      if (isLower(id)) {
        open(name).then(show);
      } else {
        turnTo(name);
      }
    }
  }

  // A small tilt that follows the mouse, so that the cube looks like a cube at rest.
  function tickTilt() {
    tilt[0] += (tiltTarget[0] - tilt[0]) * 0.1;
    tilt[1] += (tiltTarget[1] - tilt[1]) * 0.1;
    render();
    var far = Math.abs(tiltTarget[0] - tilt[0]) + Math.abs(tiltTarget[1] - tilt[1]);
    tiltFrame = far > 0.01 ? requestAnimationFrame(tickTilt) : 0;
  }

  function setTilt(x, y) {
    tiltTarget = [x, y];
    if (!tiltFrame) {
      tiltFrame = requestAnimationFrame(tickTilt);
    }
  }

  stage.addEventListener("pointermove", function (e) {
    if (!active) return;
    if (!drag) {
      if (mode === "idle" && e.pointerType === "mouse") {
        var rect = stage.getBoundingClientRect();
        var nx = ((e.clientX - rect.left) / rect.width) * 2 - 1;
        var ny = ((e.clientY - rect.top) / rect.height) * 2 - 1;
        setTilt(-ny * MAX_TILT, nx * MAX_TILT);
      }
      return;
    }
    var dx = e.clientX - drag.x;
    var dy = e.clientY - drag.y;
    if (!drag.moved) {
      if (Math.hypot(e.clientX - drag.startX, e.clientY - drag.startY) < 6) return;
      // Capture only after a real drag, so that a plain click on a link still works.
      drag.moved = true;
      mode = "drag";
      stage.setPointerCapture(e.pointerId);
      stage.classList.add("is-dragging");
      stopTurn();
      setTilt(0, 0);
    }
    var now = performance.now();
    var dt = Math.max(1, now - drag.t);
    drag.vx = drag.vx * 0.6 + (dx / dt) * 0.4;
    drag.vy = drag.vy * 0.6 + (dy / dt) * 0.4;
    drag.x = e.clientX;
    drag.y = e.clientY;
    drag.t = now;
    var len = Math.hypot(dx, dy);
    if (len > 0) {
      q = normalize(mul(axisAngle(-dy, dx, 0, len * DEG_PER_PX), q));
      render();
    }
  });

  stage.addEventListener("pointerdown", function (e) {
    if (!active || e.button !== 0 || (mode !== "idle" && mode !== "turn")) return;
    if (e.target.closest(".cube-ui")) return;
    drag = {
      startX: e.clientX,
      startY: e.clientY,
      x: e.clientX,
      y: e.clientY,
      t: performance.now(),
      vx: 0,
      vy: 0,
      moved: false,
    };
  });

  function endDrag() {
    if (!drag) return;
    var moved = drag.moved;
    var vx = drag.vx;
    var vy = drag.vy;
    drag = null;
    stage.classList.remove("is-dragging");
    if (!moved) return;
    suppressClick = true;
    setTimeout(function () {
      suppressClick = false;
    }, 0);
    // A fast flick carries on a little before the cube settles on a side.
    var speed = Math.hypot(vx, vy);
    var ahead = speed > 0 ? mul(axisAngle(-vy, vx, 0, speed * 160 * DEG_PER_PX), q) : q;
    turnTo(facing(ahead));
  }

  stage.addEventListener("pointerup", endDrag);
  stage.addEventListener("pointercancel", endDrag);
  stage.addEventListener("dragstart", function (e) {
    if (active && mode !== "open") e.preventDefault();
  });

  stage.addEventListener("pointerleave", function () {
    if (active && mode === "idle") setTilt(0, 0);
  });

  stage.addEventListener(
    "click",
    function (e) {
      if (suppressClick) {
        e.preventDefault();
        e.stopPropagation();
      }
    },
    true
  );

  // A click outside the open side closes it.
  stage.addEventListener("click", function (e) {
    if (!active || mode !== "open") return;
    if (faces[openSide].contains(e.target) || ui.contains(e.target)) return;
    close();
  });

  stage.addEventListener(
    "wheel",
    function (e) {
      if (!active) return;
      if (mode === "open" && faces[openSide].contains(e.target)) return;
      e.preventDefault();
      if (mode !== "idle" || wheelLock) return;
      wheelSum += Math.abs(e.deltaY) > Math.abs(e.deltaX) ? e.deltaY : e.deltaX;
      if (Math.abs(wheelSum) < 40) return;
      var step = wheelSum > 0 ? 1 : -1;
      wheelSum = 0;
      wheelLock = true;
      var next = ORDER[(ORDER.indexOf(current) + step + ORDER.length) % ORDER.length];
      turnTo(next).then(function () {
        setTimeout(function () {
          wheelLock = false;
          wheelSum = 0;
        }, 250);
      });
    },
    { passive: false }
  );

  cube.addEventListener("toggle", measure, true);
  cube.addEventListener("load", measure, true);

  // Up and Down scroll a long side first. They go to the next side only at the top or the
  // bottom of the side. Left and Right always go to the next side.
  function atEdge(face, key) {
    if (key === "ArrowUp") return face.scrollTop <= 1;
    if (key === "ArrowDown") return face.scrollTop + face.clientHeight >= face.scrollHeight - 1;
    return true;
  }

  document.addEventListener("keydown", function (e) {
    if (!active || e.altKey || e.metaKey || e.ctrlKey) return;
    // The screenshot preview and the guide handle their own keys.
    if (document.querySelector("dialog[open]")) return;
    if (e.key === "?" && !e.target.closest("input, textarea, select")) {
      e.preventDefault();
      showGuide();
      return;
    }
    if (mode === "open") {
      if (e.key === "Escape") {
        close();
      } else if (NET_MOVES[openSide][e.key] && atEdge(faces[openSide], e.key)) {
        e.preventDefault();
        switchOpen(NET_MOVES[openSide][e.key]);
      }
      return;
    }
    if (mode === "fold" && ARROWS[e.key]) {
      e.preventDefault();
      return;
    }
    if (ARROWS[e.key]) {
      e.preventDefault();
      if (mode === "idle") {
        arrowTurn(e.key);
      } else if (mode === "turn" && keyQueue.length < MAX_QUEUE) {
        keyQueue.push(e.key);
      }
      return;
    }
    if (mode !== "idle") return;
    var onStage = document.activeElement === stage || document.activeElement === document.body;
    if (onStage && (e.key === "Enter" || e.key === "o")) {
      e.preventDefault();
      open(current);
    }
  });

  document.addEventListener("click", function (e) {
    if (!active || e.defaultPrevented) return;
    var link = e.target.closest('a[href^="#"]');
    if (!link) return;
    var id = decodeURIComponent(link.hash.slice(1));
    if (id === "main") {
      e.preventDefault();
      stage.focus({ preventScroll: true });
    } else if (idToSide[id]) {
      e.preventDefault();
      go(id);
    }
  });

  window.addEventListener("hashchange", function () {
    var id = decodeURIComponent(location.hash.slice(1));
    if (active && idToSide[id]) go(id);
  });

  window.addEventListener("resize", function () {
    if (active) layout();
  });

  window.addEventListener("load", function () {
    if (active) measure();
  });

  function enable() {
    active = true;
    run += 1;
    mode = "idle";
    root.classList.add("is-cube");
    stage.tabIndex = 0;
    stage.setAttribute("role", "region");
    stage.setAttribute("aria-roledescription", "cube");
    stage.setAttribute("aria-label", "SpaceWarden. Six sides.");
    layout();
    setHelp();
    var id = decodeURIComponent(location.hash.slice(1));
    var start = idToSide[id] || "front";
    // Start a little turned, then settle, so the visitor sees that it is a cube.
    q = mul(axisAngle(1, -1.4, 0, 32), SIDES[start].q);
    render();
    turnTo(start, 1100).then(function () {
      if (active && mode === "idle" && idToSide[id] && isLower(id)) go(id);
    });
  }

  function disable() {
    active = false;
    run += 1;
    stopTurn();
    cancelAnimationFrame(tiltFrame);
    tiltFrame = 0;
    if (guide.open) guide.close();
    drag = null;
    keyQueue = [];
    openSide = null;
    mode = "idle";
    root.classList.remove("is-cube");
    stage.classList.remove("is-net", "is-flat", "is-reading", "is-dragging");
    stage.removeAttribute("tabindex");
    stage.removeAttribute("role");
    stage.removeAttribute("aria-roledescription");
    stage.removeAttribute("aria-label");
    stage.style.cssText = "";
    scaler.style.cssText = "";
    ORDER.forEach(function (name) {
      var face = faces[name];
      face.inert = false;
      face.classList.remove("is-open", "is-overflowing");
      face.style.cssText = "";
    });
  }

  function sync() {
    if (media.matches && !active) {
      enable();
    } else if (!media.matches && active) {
      disable();
    }
  }

  media.addEventListener("change", sync);
  sync();
})();
