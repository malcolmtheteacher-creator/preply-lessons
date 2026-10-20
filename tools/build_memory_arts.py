#!/usr/bin/env python3
"""Build the Memory Arts notebook page from content files.

  tools/memory_arts_content/part1.json  ->  memory_arts_map.html

One self-contained page laid out as a handwritten research notebook: an overview
of the whole anthology, and a Part view where an engraved plate holds ten
clickable rooms, one per extract. Threads (themes) light up rooms that share an
idea. Summaries are written in our own words; the book itself is not quoted.
Usage: python3 tools/build_memory_arts.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "memory_arts_content", "part1.json")
OUT = os.path.join(ROOT, "memory_arts_map.html")

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="series" content="Memory Arts">
<meta name="color-scheme" content="light">
<title>The Memory Arts in Renaissance England · Notebook</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Kalam:wght@300;400;700&display=swap" rel="stylesheet">
<style>
:root { --paper:#f5efdf; --sheet:#fffdf5; --ink:#1b2540; --red:#b3342d; --gold:#8a6a2c; --pencil:#6c6a66; --rule:rgba(70,100,150,.16); --margin:rgba(190,70,70,.45); --hl:rgba(255,213,60,.62); --sticky:#fff0a3; --stickyink:#3b3210; --tape:rgba(214,190,120,.66); --shadow:rgba(30,25,15,.22); }
* { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior:smooth; }
body { font-family:"Kalam","Caveat","Bradley Hand","Segoe Print",cursive; font-size:1.12rem; line-height:30px; color:var(--ink);
  background-color:var(--paper);
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .45 0 0 0 0 .38 0 0 0 0 .25 0 0 0 .10 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"), repeating-linear-gradient(to bottom, transparent 0, transparent 29px, var(--rule) 29px, var(--rule) 30px); }
.hand { font-family:"Caveat","Kalam",cursive; }
.wrap { max-width:1180px; margin:0 auto; padding:26px 18px 80px; }
button { font:inherit; color:inherit; background:none; border:0; cursor:pointer; text-align:left; }

/* title scrawled straight onto the paper */
.top { position:relative; padding:18px 4px 10px; margin-bottom:6px; }
.kicker { font-family:"Caveat",cursive; font-size:1.7rem; color:var(--red); line-height:1.1; transform:rotate(-1deg); }
.top h1 { font-family:"Caveat",cursive; font-size:4.4rem; line-height:1; font-weight:700; color:var(--ink); margin:2px 0 8px; transform:rotate(-.6deg); }
.uline { position:relative; display:inline-block; }
.uline::after { content:""; position:absolute; left:-4px; right:-6px; bottom:-8px; height:12px; background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 12' preserveAspectRatio='none'%3E%3Cpath d='M2 8 C 40 2, 80 11, 130 6 S 220 3, 298 8' fill='none' stroke='%23b3342d' stroke-width='3.2' stroke-linecap='round'/%3E%3Cpath d='M20 11 C 90 7, 170 11, 270 9' fill='none' stroke='%23b3342d' stroke-width='2' stroke-linecap='round' opacity='.7'/%3E%3C/svg%3E") no-repeat center/100% 100%; }
.sub { max-width:760px; font-size:1.12rem; }
.sub .pencil { font-family:"Caveat",cursive; font-size:1.55rem; color:var(--pencil); }
.tapeL, .tapeR { position:absolute; top:-2px; width:104px; height:26px; background:var(--tape); box-shadow:0 1px 3px rgba(0,0,0,.2); }
.tapeL { left:-26px; transform:rotate(-36deg); } .tapeR { right:-20px; transform:rotate(30deg); }

/* ink navigation */
.nav { display:flex; flex-wrap:wrap; align-items:baseline; gap:6px 14px; margin:18px 0 8px; font-family:"Caveat",cursive; font-size:1.8rem; line-height:1.2; }
.nav .back { color:var(--ink); border-bottom:2px dashed var(--ink); }
.nav .here { color:var(--red); }
.nav .sep { color:var(--pencil); }
.threads { display:flex; flex-wrap:wrap; align-items:center; gap:8px 14px; margin:4px 0 20px; }
.threads .lbl { font-family:"Caveat",cursive; font-size:1.7rem; color:var(--gold); margin-right:2px; }
.thread { font-family:"Caveat",cursive; font-size:1.55rem; line-height:1.1; padding:3px 14px 5px; border:2.5px solid var(--ink); border-radius:255px 18px 225px 18px/18px 225px 18px 255px; filter:url(#rough); transition:background .15s, transform .15s; }
.thread:hover { background:var(--hl); transform:rotate(-1.2deg); }
.thread.on { background:var(--hl); border-color:var(--red); color:var(--red); transform:rotate(-1.5deg); }

.layout { display:grid; grid-template-columns:minmax(0,1.5fr) minmax(330px,1fr); gap:30px; align-items:start; }

/* the plate, taped into the notebook */
.cap { font-family:"Caveat",cursive; font-size:1.7rem; line-height:1.15; color:var(--pencil); margin:0 6px 12px; transform:rotate(-.6deg); }
.cap b { color:var(--red); }
.plate { position:relative; line-height:0; background:var(--sheet); padding:12px 12px 14px; box-shadow:0 12px 30px var(--shadow); transform:rotate(-.5deg); }
.plate::before, .plate::after { content:""; position:absolute; width:100px; height:26px; background:var(--tape); box-shadow:0 1px 3px rgba(0,0,0,.2); z-index:4; top:-12px; }
.plate::before { left:-22px; transform:rotate(-38deg); } .plate::after { right:-22px; transform:rotate(38deg); }
.plate img { display:block; width:100%; height:auto; }
.zone { position:absolute; border:0; background:transparent; cursor:pointer; border-radius:6px; transition:background .2s, box-shadow .2s; }
.zone:hover, .zone:focus-visible { outline:none; box-shadow:inset 0 0 0 3px var(--hl), 0 0 20px rgba(255,213,60,.8); }
.zone.sel { box-shadow:inset 0 0 0 4px #fff, inset 0 0 0 7px var(--red); }
.zone.dim { background:rgba(245,239,223,.72); }
.znum { position:absolute; left:8px; top:8px; min-width:40px; height:40px; padding:0 6px; font-family:"Caveat",cursive; font-weight:700; font-size:1.55rem; line-height:36px; text-align:center; color:var(--red); background:rgba(255,253,245,.82); border:2.5px solid var(--red); border-radius:52% 48% 55% 45%/48% 55% 45% 52%; transform:rotate(-6deg); pointer-events:none; }
.zone.sel .znum { background:var(--red); color:#fff; }
.zone .ztag { position:absolute; left:50%; bottom:8px; transform:translateX(-50%) rotate(-1.5deg); font-family:"Caveat",cursive; font-size:1.45rem; line-height:1.05; background:var(--sticky); color:var(--stickyink); padding:3px 12px 4px; box-shadow:2px 3px 8px rgba(0,0,0,.4); opacity:0; transition:opacity .15s; text-align:center; width:max-content; max-width:92%; pointer-events:none; }
.zone:hover .ztag, .zone:focus-visible .ztag, .zone.sel .ztag { opacity:1; }
.margin-note { font-family:"Caveat",cursive; font-size:1.55rem; color:var(--pencil); line-height:1.15; margin:18px 8px 0; transform:rotate(.7deg); }
.margin-note svg { vertical-align:middle; margin-right:6px; }

/* the notes page on the right */
.panel { position:sticky; top:12px; background-color:var(--sheet); background-image:repeating-linear-gradient(to bottom, transparent 0, transparent 29px, var(--rule) 29px, var(--rule) 30px); box-shadow:0 12px 30px var(--shadow); padding:30px 26px 26px 66px; transform:rotate(.35deg); }
.panel::before { content:""; position:absolute; left:50px; top:0; bottom:0; border-left:2px solid var(--margin); }
.panel::after { content:""; position:absolute; top:-13px; left:52%; width:112px; height:28px; transform:translateX(-50%) rotate(-2deg); background:var(--tape); box-shadow:0 1px 3px rgba(0,0,0,.2); }
.holes { position:absolute; left:12px; top:0; bottom:0; width:22px; }
.holes i { position:absolute; left:0; width:20px; height:20px; border-radius:50%; background:var(--paper); box-shadow:inset 1px 2px 3px rgba(0,0,0,.35); }
.panel .pnum { font-family:"Caveat",cursive; font-size:1.55rem; font-weight:700; color:var(--red); line-height:1.1; }
.panel h2 { font-family:"Caveat",cursive; font-size:3rem; line-height:1; font-weight:700; color:var(--ink); margin:2px 0 4px; }
.panel h2 .uline::after { height:9px; bottom:-5px; }
.panel .who { font-family:"Caveat",cursive; font-size:1.65rem; color:var(--pencil); line-height:1.15; margin-bottom:14px; }
.panel .essence { margin-bottom:14px; }
.panel .essence::first-line { font-weight:700; }
.panel h3 { font-family:"Caveat",cursive; font-size:2rem; line-height:1; color:var(--red); margin:20px 0 6px; font-weight:700; }
.panel ul { list-style:none; padding:0; }
.panel li { position:relative; padding-left:24px; margin-bottom:8px; line-height:30px; }
.panel li::before { content:"\2013"; position:absolute; left:4px; color:var(--red); font-weight:700; }
.box2 { background:var(--sticky); color:var(--stickyink); padding:12px 16px 14px; margin-top:6px; box-shadow:2px 3px 9px rgba(0,0,0,.22); transform:rotate(-.7deg); font-family:"Caveat",cursive; font-size:1.55rem; line-height:1.25; }
.box2.m { background:transparent; box-shadow:none; border:2.5px dashed var(--gold); transform:rotate(.5deg); filter:url(#rough); }
.pills { display:flex; flex-wrap:wrap; gap:6px 10px; margin-top:6px; }
.pill { font-family:"Caveat",cursive; font-size:1.4rem; line-height:1.1; padding:2px 12px 4px; border:2.2px solid var(--ink); border-radius:255px 14px 225px 14px/14px 225px 14px 255px; filter:url(#rough); }
.pill:hover { background:var(--hl); }
.links { display:flex; flex-direction:column; gap:6px; margin-top:6px; }
.links a { display:block; text-decoration:none; color:var(--ink); font-family:"Caveat",cursive; font-size:1.7rem; line-height:1.1; padding:4px 0 2px 34px; position:relative; }
.links a::before { content:""; position:absolute; left:0; top:12px; width:26px; height:14px; background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 26 14'%3E%3Cpath d='M1 8 C 8 5, 14 9, 23 7 M17 2 C 20 4, 22 6, 24 7 C 22 9, 19 11, 16 13' fill='none' stroke='%23b3342d' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") no-repeat center/contain; }
.links a span { border-bottom:2px dashed var(--ink); }
.links a:hover span { background:var(--hl); }
.links a small { display:block; font-family:"Kalam",cursive; font-size:.88rem; line-height:20px; color:var(--pencil); margin-top:2px; }
.navrow { display:flex; justify-content:space-between; gap:10px; margin-top:18px; font-family:"Caveat",cursive; font-size:1.8rem; line-height:1; }
.navrow button { color:var(--red); font-weight:700; }
.navrow button:hover { background:var(--hl); }
.hint { font-family:"Caveat",cursive; font-size:1.55rem; color:var(--pencil); line-height:1.2; }

/* overview + list */
.map svg { display:block; width:100%; height:auto; }
.node { cursor:pointer; outline:none; }
.node rect.box { fill:var(--sheet); stroke:var(--ink); stroke-width:3; filter:url(#rough); transition:fill .15s; }
.node:hover rect.box, .node:focus rect.box { fill:var(--hl); stroke:var(--red); }
.node.soon rect.box { stroke-dasharray:9 7; }
.node .num { fill:var(--red); font-family:"Caveat",cursive; font-weight:700; font-size:21px; }
.node .ttl { fill:var(--ink); font-family:"Caveat",cursive; font-weight:700; font-size:30px; }
.node .sub { fill:var(--pencil); font-family:"Kalam",cursive; font-size:13px; }
.spoke { stroke:var(--pencil); stroke-width:2.2; stroke-dasharray:2 9; stroke-linecap:round; opacity:.8; }
.hub ellipse { fill:var(--hl); stroke:var(--red); stroke-width:3.5; filter:url(#rough); }
.hub text { fill:var(--ink); text-anchor:middle; font-family:"Caveat",cursive; font-weight:700; }
.list { display:none; }
.partcards { display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:10px; margin-top:6px; }
.pc { font-family:"Caveat",cursive; font-size:1.55rem; line-height:1.1; padding:8px 14px 10px; border:2.5px solid var(--ink); border-radius:255px 18px 225px 18px/18px 225px 18px 255px; background:var(--sheet); filter:url(#rough); }
.pc b { display:block; } .pc span { font-family:"Kalam",cursive; font-size:.88rem; color:var(--pencil); line-height:20px; display:block; }
.pc.soon { border-style:dashed; opacity:.75; }
.note { text-align:center; font-family:"Caveat",cursive; font-size:1.55rem; color:var(--pencil); margin-top:36px; line-height:1.25; }
.note a { color:var(--red); font-weight:700; }
@media (max-width:860px) {
  .layout { grid-template-columns:1fr; gap:26px; }
  .top h1 { font-size:2.9rem; } .panel { position:static; transform:none; padding:28px 18px 24px 52px; } .panel::before { left:38px; }
  .panel h2 { font-size:2.4rem; } .holes { left:6px; }
  .map { display:none; } .list { display:block; }
  body[data-view="part"] .map { display:block; } body[data-view="part"] .list { display:none; }
  .znum { min-width:28px; height:28px; line-height:24px; font-size:1.05rem; left:4px; top:4px; border-width:2px; }
  .zone .ztag { font-size:1.05rem; bottom:3px; padding:1px 6px 2px; }
  .plate::before, .plate::after { width:64px; height:18px; top:-8px; }
  .cap { margin-bottom:20px; } .tapeL, .tapeR { width:70px; }
}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><filter id="rough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.2"/></filter></svg>
<div class="wrap">
  <header class="top">
    <span class="tapeL"></span><span class="tapeR"></span>
    <div class="kicker">notes from a very large project &middot; england, 1500&ndash;1700</div>
    <h1>The Memory Arts in <span class="uline">Renaissance England</span></h1>
    <p class="sub">How people in Shakespeare's England trained their memories with imagined places, vivid pictures and even their own hands. <span class="pencil">choose a part, then a book, and follow the threads &rarr;</span></p>
  </header>

  <div class="nav" id="crumbs"></div>
  <div class="threads" id="themes" hidden></div>

  <div class="layout">
    <div>
      <div class="map" id="map"></div>
      <div class="list" id="list"></div>
    </div>
    <aside class="panel" id="panel" aria-live="polite"></aside>
  </div>

  <p class="note"><a href="memory_arts_notes_method.html">&rarr; and my notes on how to build a memory palace</a><br>everything here is in my own words; the books are worth reading themselves &mdash; <a id="booklink" target="_blank" rel="noopener"></a></p>
</div>

<script id="data" type="application/json">__DATA__</script>
<script>
var D = JSON.parse(document.getElementById('data').textContent);
var NS = 'http://www.w3.org/2000/svg';
var state = { view: 'overview', part: null, sel: null, theme: null };
var W = 1000, H = 760, CX = 500, CY = 380;

var $ = function (id) { return document.getElementById(id); };
function el(tag, attrs, parent) {
  var e = document.createElementNS(NS, tag);
  for (var k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}
function esc(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
function find(id) { return D.extracts.filter(function (e) { return e.id === id; })[0]; }
function ringPos(i, n, rx, ry) { var a = -Math.PI / 2 + (i * 2 * Math.PI / n); return { x: CX + rx * Math.cos(a), y: CY + ry * Math.sin(a) }; }
function themeLabel(id) { return D.themes.filter(function (t) { return t.id === id; })[0].label; }
function clean(s) { return s.replace(/[\[\]]/g, ''); }
function wrap(text, max) {
  var words = text.split(' '), lines = [], cur = '';
  words.forEach(function (w) { if ((cur + ' ' + w).trim().length > max) { lines.push(cur); cur = w; } else { cur = (cur + ' ' + w).trim(); } });
  if (cur) lines.push(cur);
  return lines;
}

function node(g, x, y, w, h, o) {
  var n = el('g', { 'class': 'node' + (o.soon ? ' soon' : ''), tabindex: 0, role: 'button', 'aria-label': o.label, transform: 'translate(' + (x - w / 2) + ',' + (y - h / 2) + ')' }, g);
  el('rect', { 'class': 'box', width: w, height: h, rx: 12 }, n);
  var t = el('text', { 'class': 'num', x: 14, y: 26 }, n); t.textContent = o.num;
  var lines = wrap(o.title, o.wrap || 18).slice(0, 2);
  lines.forEach(function (ln, i) { var tt = el('text', { 'class': 'ttl', x: 14, y: 54 + i * 28 }, n); tt.textContent = ln; });
  var s = el('text', { 'class': 'sub', x: 14, y: 54 + lines.length * 28 }, n); s.textContent = o.sub;
  n.addEventListener('click', o.onclick);
  n.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); o.onclick(); } });
  return n;
}

function drawOverview() {
  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Map of the six parts of the anthology' });
  var spokes = el('g', {}, svg), nodes = el('g', {}, svg);
  D.parts.forEach(function (p, i) {
    var pos = ringPos(i, D.parts.length, 340, 275);
    el('line', { 'class': 'spoke', x1: CX, y1: CY, x2: pos.x, y2: pos.y }, spokes);
    node(nodes, pos.x, pos.y, 250, 104, { num: 'part ' + p.id, title: p.title, wrap: 19, sub: p.count + ' extracts' + (p.live ? '' : ' · coming soon'), soon: !p.live, label: 'Part ' + p.id + ': ' + p.title, onclick: function () { if (p.live) go('part'); else showPart(p); } });
  });
  var hub = el('g', { 'class': 'hub' }, svg);
  el('ellipse', { cx: CX, cy: CY, rx: 150, ry: 80 }, hub);
  var a = el('text', { x: CX, y: CY - 4, 'font-size': 34 }, hub); a.textContent = 'The Memory Arts';
  var b = el('text', { x: CX, y: CY + 30, 'font-size': 26 }, hub); b.textContent = 'in Renaissance England';
  return svg;
}

function drawRing() {
  var ex = D.extracts;
  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Mindmap of the ten extracts in Part I' });
  var spokes = el('g', {}, svg), nodes = el('g', {}, svg);
  ex.forEach(function (e, i) {
    var pos = ringPos(i, ex.length, 330, 275);
    el('line', { 'class': 'spoke', x1: CX, y1: CY, x2: pos.x, y2: pos.y }, spokes);
    node(nodes, pos.x, pos.y, 220, 100, { num: e.id, title: e.short, wrap: 17, sub: clean(e.author) + ' · ' + e.year, soon: !e.live, label: e.id + ' ' + e.short, onclick: function () { select(e.id); } });
  });
  var hub = el('g', { 'class': 'hub' }, svg);
  el('ellipse', { cx: CX, cy: CY, rx: 110, ry: 62 }, hub);
  var b = el('text', { x: CX, y: CY + 8, 'font-size': 30 }, hub); b.textContent = 'Part I';
  return svg;
}

function drawPlate() {
  var wrapEl = document.createElement('div');
  var cap = document.createElement('div'); cap.className = 'cap';
  if (state.theme) {
    var n = D.extracts.filter(function (e) { return e.themes.indexOf(state.theme) >= 0; }).length;
    cap.innerHTML = 'thread: <b>' + esc(themeLabel(state.theme)) + '</b> — ' + n + ' rooms light up';
  } else {
    cap.innerHTML = 'part I: ten guides, ten rooms. <b>tap a room</b> to open its notes';
  }
  wrapEl.appendChild(cap);
  var plate = document.createElement('div'); plate.className = 'plate';
  var img = document.createElement('img'); img.src = D.plate.src; img.alt = D.plate.alt;
  img.onerror = function () { wrapEl.replaceChild(drawRing(), plate); };
  plate.appendChild(img);
  D.extracts.forEach(function (e) {
    var z = document.createElement('button'); z.type = 'button';
    var inTheme = state.theme ? e.themes.indexOf(state.theme) >= 0 : true;
    z.className = 'zone' + (state.sel === e.id ? ' sel' : '') + (inTheme ? '' : ' dim');
    z.style.left = e.zone[0] + '%'; z.style.top = e.zone[1] + '%'; z.style.width = e.zone[2] + '%'; z.style.height = e.zone[3] + '%';
    z.setAttribute('aria-label', e.id + ' ' + e.short + ', ' + clean(e.author));
    var num = document.createElement('span'); num.className = 'znum'; num.textContent = e.id.replace('I.', '');
    var t = document.createElement('span'); t.className = 'ztag';
    t.textContent = e.id + ' · ' + e.short + (e.live ? '' : ' (notes coming)');
    z.appendChild(num); z.appendChild(t);
    z.onclick = function () { select(e.id); };
    plate.appendChild(z);
  });
  wrapEl.appendChild(plate);
  var mn = document.createElement('div'); mn.className = 'margin-note';
  mn.innerHTML = '<svg width="46" height="26" viewBox="0 0 46 26" aria-hidden="true"><path d="M44 4 C 30 2, 14 8, 5 20 M5 20 L13 17 M5 20 L7 11" fill="none" stroke="#b3342d" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>the gold thread is the walk through the palace, in order';
  wrapEl.appendChild(mn);
  return wrapEl;
}

function drawList() {
  var box = $('list'); box.innerHTML = '';
  var items = state.view === 'overview' ? D.parts : D.extracts;
  var g = document.createElement('div'); g.className = 'partcards';
  items.forEach(function (it) {
    var b = document.createElement('button'); b.className = 'pc' + (!it.live ? ' soon' : '');
    if (state.view === 'overview') {
      b.innerHTML = '<b>part ' + esc(it.id) + ' · ' + esc(it.title) + '</b><span>' + it.count + ' extracts' + (it.live ? '' : ' · coming soon') + '</span>';
      b.onclick = function () { if (it.live) go('part'); else showPart(it); };
    } else {
      var inT = !state.theme || it.themes.indexOf(state.theme) >= 0;
      b.style.opacity = inT ? '' : '.35';
      b.innerHTML = '<b>' + esc(it.id) + ' · ' + esc(it.short) + '</b><span>' + esc(clean(it.author)) + ' · ' + esc(it.year) + '</span>';
      b.onclick = function () { select(it.id); };
    }
    g.appendChild(b);
  });
  box.appendChild(g);
}

function crumbs() {
  var c = $('crumbs'); c.innerHTML = '';
  var a = document.createElement('button'); a.className = 'back'; a.textContent = '← the whole book'; a.onclick = function () { go('overview'); };
  c.appendChild(a);
  if (state.view === 'part') {
    var s = document.createElement('span'); s.className = 'sep'; s.textContent = '/'; c.appendChild(s);
    var p = document.createElement('span'); p.className = 'here'; p.textContent = 'part I · the art of memory'; c.appendChild(p);
  }
  var th = $('themes'); th.innerHTML = ''; th.hidden = state.view !== 'part';
  if (state.view === 'part') {
    var l = document.createElement('span'); l.className = 'lbl'; l.textContent = 'follow a thread:'; th.appendChild(l);
    D.themes.forEach(function (t) {
      var b = document.createElement('button'); b.className = 'thread' + (state.theme === t.id ? ' on' : ''); b.textContent = t.label.toLowerCase();
      b.onclick = function () { state.theme = state.theme === t.id ? null : t.id; render(); };
      th.appendChild(b);
    });
  }
}

function holes() { return '<div class="holes"><i style="top:70px"></i><i style="top:50%"></i><i style="bottom:70px"></i></div>'; }

function linksFor(e) {
  var out = '<a href="' + D.book.url + '" target="_blank" rel="noopener"><span>read it in the book</span><small>part I, extract ' + esc(e.id) + ', printed pages ' + esc(e.pages) + ' in the Cambridge edition</small></a>';
  out += '<a href="https://archive.org/search?query=' + encodeURIComponent(e.search) + '" target="_blank" rel="noopener"><span>look for the original</span><small>search the Internet Archive for the early printed text</small></a>';
  (e.wiki || []).forEach(function (w) { out += '<a href="' + w[1] + '" target="_blank" rel="noopener"><span>background: ' + esc(w[0].toLowerCase()) + '</span><small>Wikipedia</small></a>'; });
  return out;
}

function panelExtract(e) {
  var p = $('panel');
  var i = D.extracts.indexOf(e), prev = D.extracts[i - 1], next = D.extracts[i + 1];
  var h = holes() + '<div class="pnum">part I · ' + esc(e.id) + ' · pp. ' + esc(e.pages) + '</div><h2><span class="uline">' + esc(e.short) + '</span></h2><div class="who">' + esc(clean(e.author)) + ', ' + esc(e.year) + '</div>';
  if (e.live) {
    h += '<p class="essence">' + esc(e.essence) + '</p><h3>what it says</h3><ul>' + e.points.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>';
    h += '<h3>picture it</h3><div class="box2">' + esc(e.picture) + '</div><h3>try it yourself</h3><div class="box2">' + esc(e.tryit) + '</div>';
    if (e.note) h += '<h3>a note from the margin</h3><div class="box2 m">' + esc(e.note) + '</div>';
    h += '<h3>threads</h3><div class="pills">' + e.themes.map(function (t) { return '<button class="pill" data-t="' + t + '">' + esc(themeLabel(t).toLowerCase()) + '</button>'; }).join('') + '</div>';
  } else {
    h += '<p class="essence">my notes on this one are still being written. In the meantime you can find it in the book, or look for the original.</p>';
  }
  h += '<h3>go to the book</h3><div class="links">' + linksFor(e) + '</div>';
  h += '<div class="navrow"><button ' + (prev ? 'data-go="' + prev.id + '"' : 'disabled style="opacity:.25"') + '>← ' + (prev ? esc(prev.id) : '') + '</button><button ' + (next ? 'data-go="' + next.id + '"' : 'disabled style="opacity:.25"') + '>' + (next ? esc(next.id) : '') + ' →</button></div>';
  p.innerHTML = h;
  p.querySelectorAll('[data-go]').forEach(function (b) { b.onclick = function () { select(b.getAttribute('data-go')); }; });
  p.querySelectorAll('.pill').forEach(function (b) { b.onclick = function () { state.theme = b.getAttribute('data-t'); render(); }; });
}

function showPart(p) {
  $('panel').innerHTML = holes() + '<div class="pnum">part ' + esc(p.id) + '</div><h2><span class="uline">' + esc(p.title) + '</span></h2><p class="essence" style="margin-top:12px">' + esc(p.blurb) + '</p><p class="hint">' + p.count + ' extracts. my notes on this part are coming soon.</p><h3>go to the book</h3><div class="links"><a href="' + D.book.url + '" target="_blank" rel="noopener"><span>read it in the book</span><small>' + esc(D.book.publisher) + '</small></a></div>';
}

function panelHome() {
  var h = holes() + '<div class="pnum">start here</div><h2><span class="uline">' + esc(D.book.title) + '</span></h2><div class="who">' + esc(D.book.subtitle) + ' · ' + esc(D.book.editors) + '</div>';
  if (state.view === 'overview') {
    h += '<p class="essence">An anthology of seventy or so writers from 1500 to 1700, gathered in six parts. Each extract shows how English readers thought about remembering: with imagined buildings, strange pictures, notebooks, prayers and poems.</p><p class="hint">begin with part I. the others are coming.</p>';
  } else {
    h += '<p class="essence">Ten guides to building a memory. Tap a room in the picture to see what that guide says and how to find it. Then follow a thread to see which books share an idea.</p>';
  }
  h += '<div class="links"><a href="memory_arts_notes_method.html"><span>my notes: how to build a memory palace</span><small>the method, step by step</small></a><a href="' + D.book.url + '" target="_blank" rel="noopener"><span>open the book</span><small>Cambridge University Press, 2016</small></a></div>';
  $('panel').innerHTML = h;
}

function render() {
  crumbs();
  var m = $('map'); m.innerHTML = '';
  document.body.setAttribute('data-view', state.view);
  m.appendChild(state.view === 'overview' ? drawOverview() : drawPlate());
  drawList();
  if (state.view === 'part' && state.sel) panelExtract(find(state.sel)); else panelHome();
  try { history.replaceState(null, '', state.sel ? '#' + state.sel : (state.view === 'part' ? '#part-I' : location.pathname)); } catch (e) {}
}
function go(view) { state.view = view; state.sel = null; state.theme = null; render(); }
function select(id) { state.view = 'part'; state.sel = id; render(); if (window.innerWidth <= 860) $('panel').scrollIntoView({ behavior: 'smooth', block: 'start' }); }

$('booklink').href = D.book.url; $('booklink').textContent = 'open the book';
var h = (location.hash || '').replace('#', '');
if (h && find(h)) { state.view = 'part'; state.sel = h; } else if (h === 'part-I') { state.view = 'part'; }
render();
</script>
</body>
</html>
"""


def main():
    with open(SRC, encoding="utf-8") as f:
        data = json.load(f)
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    out = TEMPLATE.replace("__DATA__", payload)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote", OUT, f"({len(out):,} bytes)")


if __name__ == "__main__":
    main()
