#!/usr/bin/env python3
"""Build the Memory Arts mindmap page from content files.

  tools/memory_arts_content/part1.json  ->  memory_arts_map.html

One self-contained page: an overview of the whole anthology, and a Part view
where each extract is a node in a mindmap. Themes draw threads between nodes.
Summaries are written in our own words; the book itself is not quoted.
Usage: python3 tools/build_memory_arts.py
"""
import json, os, html, urllib.parse

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
<title>The Memory Arts in Renaissance England · A Map</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Kalam:wght@400;700&display=swap" rel="stylesheet">
<style>
:root { --ink:#16263d; --gold:#8a6a2c; --paper:#faf7f0; --card:#ffffff; --line:#cfc6b0; --soft:#f1ede2; --muted:#5b5b5b; --text:#1f2933; --shadow:rgba(22,38,61,.14); }
:root[data-theme="dark"] { --ink:#e8e2d2; --gold:#d3b36a; --paper:#0f1724; --card:#17233a; --line:#33425e; --soft:#1d2b45; --muted:#a6b0c2; --text:#e6e9ef; --shadow:rgba(0,0,0,.4); }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --ink:#e8e2d2; --gold:#d3b36a; --paper:#0f1724; --card:#17233a; --line:#33425e; --soft:#1d2b45; --muted:#a6b0c2; --text:#e6e9ef; --shadow:rgba(0,0,0,.4); } }
:root { --sheet:#fffdf6; --rule:rgba(70,100,150,.13); --margin:rgba(190,70,70,.35); --sticky:#fff1a8; --sticky-ink:#3d3511; --dimveil:rgba(250,247,240,.66); }
:root[data-theme="dark"] { --sheet:#1a2740; --rule:rgba(140,170,220,.10); --margin:rgba(220,110,110,.35); --sticky:#5a4a1c; --sticky-ink:#fbeab0; --dimveil:rgba(15,23,36,.7); }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --sheet:#1a2740; --rule:rgba(140,170,220,.10); --margin:rgba(220,110,110,.35); --sticky:#5a4a1c; --sticky-ink:#fbeab0; --dimveil:rgba(15,23,36,.7); } }
* { margin:0; padding:0; box-sizing:border-box; }
.hand { font-family:"Caveat","Kalam","Bradley Hand","Segoe Print",cursive; }
body { font-family:"Segoe UI",Tahoma,Geneva,Verdana,sans-serif; background-color:var(--paper); background-image:repeating-linear-gradient(to bottom, transparent 0, transparent 35px, var(--rule) 35px, var(--rule) 36px); color:var(--text); line-height:1.6; }
.container { max-width:1180px; margin:0 auto; padding:20px 16px 60px; }
header { position:relative; overflow:hidden; text-align:center; color:#fff; padding:46px 24px 40px; margin-bottom:22px; border:1px solid var(--line); border-radius:6px; box-shadow:0 6px 22px var(--shadow); background:linear-gradient(135deg,#2f5f86 0%,#16263d 82%); }
header::after { content:""; position:absolute; inset:0; background-image:radial-gradient(rgba(255,255,255,.10) 1.2px,transparent 1.4px); background-size:9px 9px; pointer-events:none; }
header > * { position:relative; z-index:1; }
.tag { display:inline-block; padding:5px 15px; background:rgba(255,255,255,.18); border-radius:4px; font-size:.78rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:12px; }
h1 { font-size:2.6rem; line-height:1.08; margin-bottom:10px; letter-spacing:1px; }
.subtitle { font-size:1.08rem; max-width:720px; margin:0 auto; opacity:.96; }
.crumbs { display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin-bottom:12px; font-size:.95rem; }
.crumbs button, .chip { font:inherit; cursor:pointer; border:2px solid var(--ink); background:var(--card); color:var(--ink); border-radius:4px; padding:5px 14px; font-weight:700; }
.crumbs button:hover, .chip:hover { background:var(--soft); }
.chip.on { background:var(--gold); border-color:var(--gold); color:#fff; }
.themes { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:12px; align-items:center; }
.themes .lbl { font-size:.8rem; letter-spacing:.14em; text-transform:uppercase; font-weight:800; color:var(--gold); margin-right:4px; }
.layout { display:grid; grid-template-columns:minmax(0,1.5fr) minmax(320px,1fr); gap:22px; align-items:start; }
.map { background:var(--card); border:1px solid var(--line); border-radius:6px; box-shadow:0 6px 22px var(--shadow); padding:8px; }
.map svg { display:block; width:100%; height:auto; font-family:inherit; }
.node { cursor:pointer; outline:none; }
.node rect.box { fill:var(--paper); stroke:var(--ink); stroke-width:2; transition:fill .15s, stroke .15s, opacity .15s; }
.node:hover rect.box, .node:focus rect.box { stroke:var(--gold); stroke-width:3; }
.node.sel rect.box { fill:var(--ink); }
.node.sel text { fill:var(--paper) !important; }
.node.dim { opacity:.28; }
.node.soon rect.box { stroke-dasharray:5 4; }
.node .num { fill:var(--gold); font-weight:800; font-size:13px; }
.node .ttl { fill:var(--ink); font-weight:700; font-size:14px; }
.node .sub { fill:var(--muted); font-size:11.5px; }
.badge { fill:var(--gold); }
.spoke { stroke:var(--gold); stroke-width:2; stroke-dasharray:3 8; stroke-linecap:round; opacity:.55; transition:opacity .2s; }
.spoke.hot { opacity:1; stroke-width:3.5; stroke-dasharray:none; }
.spoke.dim { opacity:.1; }
.hub rect, .hub ellipse { fill:var(--ink); }
.hub text { fill:var(--paper); text-anchor:middle; }
.panel { position:sticky; top:12px; background-color:var(--sheet); background-image:repeating-linear-gradient(to bottom, transparent 0, transparent 29px, var(--rule) 29px, var(--rule) 30px); border:1px solid var(--line); border-radius:3px; box-shadow:0 8px 24px var(--shadow); padding:24px 24px 24px 44px; transform:rotate(.25deg); }
.panel::before { content:""; position:absolute; left:30px; top:0; bottom:0; border-left:2px solid var(--margin); }
.panel::after { content:""; position:absolute; top:-12px; left:50%; width:110px; height:26px; transform:translateX(-50%) rotate(-2deg); background:rgba(214,190,120,.55); box-shadow:0 1px 3px rgba(0,0,0,.18); }
.panel .pnum { font-family:"Caveat","Kalam",cursive; font-size:1.25rem; font-weight:700; color:var(--gold); margin-bottom:0; }
.panel h2 { font-size:1.7rem; line-height:1.15; color:var(--ink); margin-bottom:2px; }
.panel .who { font-family:"Caveat","Kalam",cursive; font-size:1.3rem; color:var(--muted); margin-bottom:12px; }
.panel .essence { font-size:1.04rem; margin-bottom:14px; }
.panel h3 { font-family:"Caveat","Kalam",cursive; font-size:1.55rem; font-weight:700; color:var(--gold); margin:16px 0 4px; text-decoration:underline wavy rgba(138,106,44,.35); text-underline-offset:6px; }
.panel ul { padding-left:20px; } .panel li { margin-bottom:6px; }
.box2 { background:var(--sticky); color:var(--sticky-ink); padding:12px 16px; border-radius:2px; margin-top:6px; box-shadow:2px 3px 8px rgba(0,0,0,.16); transform:rotate(-.6deg); font-family:"Caveat","Kalam",cursive; font-size:1.3rem; line-height:1.35; }
.box2.margin { background:transparent; box-shadow:none; border:2px dashed var(--gold); transform:rotate(.4deg); }
.plate { position:relative; line-height:0; background:var(--sheet); padding:12px 12px 14px; border:1px solid var(--line); box-shadow:0 10px 30px var(--shadow); transform:rotate(-.35deg); }
.plate::before, .plate::after { content:""; position:absolute; width:96px; height:24px; background:rgba(214,190,120,.6); box-shadow:0 1px 3px rgba(0,0,0,.2); z-index:3; }
.plate::before { top:-10px; left:-18px; transform:rotate(-38deg); } .plate::after { top:-10px; right:-18px; transform:rotate(38deg); }
.plate img { display:block; width:100%; height:auto; }
.plate-wrap { position:relative; }
.zone { position:absolute; border:0; background:transparent; cursor:pointer; border-radius:6px; transition:background .2s, box-shadow .2s; }
.zone:hover, .zone:focus-visible { outline:none; box-shadow:inset 0 0 0 3px var(--gold), 0 0 22px rgba(212,175,55,.65); }
.zone.sel { box-shadow:inset 0 0 0 3px #fff, inset 0 0 0 6px var(--gold), 0 0 26px rgba(212,175,55,.8); }
.zone.dim { background:var(--dimveil); }
.zone .ztag { position:absolute; left:50%; bottom:8px; transform:translateX(-50%) rotate(-1.5deg); font-family:"Caveat","Kalam",cursive; font-size:1.3rem; line-height:1.1; background:var(--sticky); color:var(--sticky-ink); padding:2px 12px; border-radius:2px; box-shadow:2px 3px 8px rgba(0,0,0,.4); opacity:0; transition:opacity .15s; white-space:normal; text-align:center; width:max-content; max-width:92%; pointer-events:none; }
.zone:hover .ztag, .zone:focus-visible .ztag, .zone.sel .ztag { opacity:1; }
.caption { font-family:"Caveat","Kalam",cursive; font-size:1.45rem; color:var(--muted); margin:0 4px 10px; line-height:1.2; }
.caption b { color:var(--gold); }
.pills { display:flex; flex-wrap:wrap; gap:6px; margin-top:6px; }
.pill { font-size:.78rem; font-weight:700; background:var(--ink); color:var(--paper); border-radius:4px; padding:2px 10px; cursor:pointer; border:0; font-family:inherit; }
.links { display:flex; flex-direction:column; gap:8px; margin-top:6px; }
.links a { display:block; text-decoration:none; padding:9px 14px; border:2px solid var(--ink); border-radius:4px; color:var(--ink); font-weight:700; background:var(--card); }
.links a:hover { background:var(--gold); border-color:var(--gold); color:#fff; }
.links a small { display:block; font-weight:400; font-size:.82rem; opacity:.85; }
.navrow { display:flex; justify-content:space-between; gap:10px; margin-top:16px; }
.navrow button { font:inherit; cursor:pointer; border:0; background:none; color:var(--gold); font-weight:800; }
.hint { color:var(--muted); font-size:.95rem; }
.list { display:none; }
.partcards { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:10px; margin-top:12px; }
.pc { text-align:left; font:inherit; cursor:pointer; background:var(--card); border:1px solid var(--line); border-radius:6px; padding:12px 14px; color:var(--text); }
.pc b { display:block; color:var(--ink); } .pc span { font-size:.86rem; color:var(--muted); }
.pc.soon { opacity:.6; }
.note { text-align:center; color:var(--muted); font-size:.9rem; margin-top:26px; }
.note a { color:var(--gold); font-weight:700; }
@media (max-width:860px) {
  .layout { grid-template-columns:1fr; } .panel { position:static; }
  h1 { font-size:1.9rem; }
  .chip, .crumbs button { padding:3px 10px; font-size:.85rem; }
  .map { display:none; } .list { display:block; }
  body[data-view="part"] .map { display:block; } body[data-view="part"] .list { display:none; }
  .zone .ztag { font-size:1rem; bottom:3px; padding:0 6px; }
  .caption { margin-bottom:24px; }
  .plate::before, .plate::after { width:64px; height:18px; top:-8px; }
  .panel { transform:none; padding-left:36px; } .panel::before { left:22px; }
}
</style>
</head>
<body>
<div class="container">
  <header>
    <span class="tag">A map of the sources &middot; England 1500&ndash;1700</span>
    <h1>The Memory Arts in<br>Renaissance England</h1>
    <p class="subtitle">How people in Shakespeare's England trained their memories with imagined places, vivid pictures and even their own hands. Choose a part, then a book, and follow the threads.</p>
    <p class="hand" style="font-size:1.7rem;margin-top:10px;opacity:.9">notes toward a memory palace &mdash; still growing</p>
  </header>

  <div class="crumbs" id="crumbs"></div>
  <div class="themes" id="themes" hidden></div>

  <div class="layout">
    <div>
      <div class="map" id="map"></div>
      <div class="list" id="list"></div>
    </div>
    <aside class="panel" id="panel" aria-live="polite"></aside>
  </div>

  <p class="note"><a href="memory_arts_notes_method.html">New: notes on how to build a memory palace &rarr;</a><br>Every summary here is written in our own words. To read the extracts themselves, use <a id="booklink" target="_blank" rel="noopener"></a>, or search for the original early printed books from the links beside each entry.</p>
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
function ringPos(i, n, rx, ry) {
  var a = -Math.PI / 2 + (i * 2 * Math.PI / n);
  return { x: CX + rx * Math.cos(a), y: CY + ry * Math.sin(a) };
}
function themeLabel(id) { return D.themes.filter(function (t) { return t.id === id; })[0].label; }
function wrap(text, max) {
  var words = text.split(' '), lines = [], cur = '';
  words.forEach(function (w) {
    if ((cur + ' ' + w).trim().length > max) { lines.push(cur); cur = w; } else { cur = (cur + ' ' + w).trim(); }
  });
  if (cur) lines.push(cur);
  return lines;
}

function node(g, x, y, w, h, o) {
  var n = el('g', { 'class': 'node' + (o.soon ? ' soon' : '') + (o.dim ? ' dim' : '') + (o.sel ? ' sel' : ''), tabindex: 0, role: 'button', 'aria-label': o.label, transform: 'translate(' + (x - w / 2) + ',' + (y - h / 2) + ')' }, g);
  el('rect', { 'class': 'box', width: w, height: h, rx: 10 }, n);
  var t = el('text', { 'class': 'num', x: 12, y: 19 }, n); t.textContent = o.num;
  var lines = wrap(o.title, o.wrap || 22).slice(0, 2);
  lines.forEach(function (ln, i) { var tt = el('text', { 'class': 'ttl', x: 12, y: 38 + i * 16 }, n); tt.textContent = ln; });
  var s = el('text', { 'class': 'sub', x: 12, y: 38 + lines.length * 16 + 2 }, n); s.textContent = o.sub;
  n.addEventListener('click', o.onclick);
  n.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); o.onclick(); } });
  return n;
}

function drawOverview() {
  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Map of the six parts of the anthology' });
  var spokes = el('g', {}, svg), nodes = el('g', {}, svg);
  D.parts.forEach(function (p, i) {
    var pos = ringPos(i, D.parts.length, 340, 270);
    el('line', { 'class': 'spoke', x1: CX, y1: CY, x2: pos.x, y2: pos.y }, spokes);
    node(nodes, pos.x, pos.y, 220, 78, {
      num: 'PART ' + p.id, title: p.title, wrap: 24, sub: p.count + ' extracts' + (p.live ? '' : ' · coming soon'),
      soon: !p.live, label: 'Part ' + p.id + ': ' + p.title,
      onclick: function () { if (p.live) go('part', p.id); else showPart(p); }
    });
  });
  var hub = el('g', { 'class': 'hub' }, svg);
  el('ellipse', { cx: CX, cy: CY, rx: 150, ry: 78 }, hub);
  var a = el('text', { x: CX, y: CY - 8, 'font-size': 21, 'font-weight': 700 }, hub); a.textContent = 'The Memory Arts';
  var b = el('text', { x: CX, y: CY + 16, 'font-size': 13 }, hub); b.textContent = 'in Renaissance England';
  return svg;
}

function drawPlate() {
  var wrapEl = document.createElement('div'); wrapEl.className = 'plate-wrap';
  var cap = document.createElement('div'); cap.className = 'caption';
  if (state.theme) {
    var n = D.extracts.filter(function (e) { return e.themes.indexOf(state.theme) >= 0; }).length;
    cap.innerHTML = 'Thread: <b>' + esc(themeLabel(state.theme)) + '</b> — ' + n + ' rooms light up.';
  } else {
    cap.innerHTML = 'Part I: ten guides, ten rooms. <b>Tap a room</b> to open its notes.';
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
    z.setAttribute('aria-label', e.id + ' ' + e.short + ', ' + e.author.replace(/[\[\]]/g, ''));
    var t = document.createElement('span'); t.className = 'ztag';
    t.textContent = e.id + ' · ' + e.short + (e.live ? '' : ' (notes coming)');
    z.appendChild(t);
    z.onclick = function () { select(e.id); };
    plate.appendChild(z);
  });
  wrapEl.appendChild(plate);
  return wrapEl;
}

function drawRing() {
  var ex = D.extracts;
  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Mindmap of the ten extracts in Part I' });
  var spokes = el('g', {}, svg), nodes = el('g', {}, svg);
  ex.forEach(function (e, i) {
    var pos = ringPos(i, ex.length, 330, 275);
    var inTheme = state.theme ? e.themes.indexOf(state.theme) >= 0 : false;
    var cls = 'spoke' + (state.theme ? (inTheme ? ' hot' : ' dim') : '');
    el('line', { 'class': cls, x1: CX, y1: CY, x2: pos.x, y2: pos.y }, spokes);
    node(nodes, pos.x, pos.y, 196, 74, {
      num: e.id, title: e.short, wrap: 24, sub: e.author.replace(/[\[\]]/g, '') + ' · ' + e.year,
      soon: !e.live, dim: state.theme && !inTheme, sel: state.sel === e.id, label: e.id + ' ' + e.short + ', ' + e.author,
      onclick: function () { select(e.id); }
    });
  });
  var hub = el('g', { 'class': 'hub' }, svg);
  el('ellipse', { cx: CX, cy: CY, rx: 120, ry: 66 }, hub);
  if (state.theme) {
    var t = el('text', { x: CX, y: CY - 4, 'font-size': 18, 'font-weight': 700 }, hub);
    wrap(themeLabel(state.theme), 18).forEach(function (ln, i) { var s = el('tspan', { x: CX, dy: i === 0 ? 0 : 20 }, t); s.textContent = ln; });
    var c = el('text', { x: CX, y: CY + 38, 'font-size': 12 }, hub);
    c.textContent = ex.filter(function (e) { return e.themes.indexOf(state.theme) >= 0; }).length + ' threads';
  } else {
    var a = el('text', { x: CX, y: CY - 6, 'font-size': 14, 'font-weight': 700, 'letter-spacing': 2 }, hub); a.textContent = 'PART I';
    var b = el('text', { x: CX, y: CY + 18, 'font-size': 18, 'font-weight': 700 }, hub); b.textContent = 'The art of memory';
  }
  return svg;
}

function drawList() {
  var box = $('list'); box.innerHTML = '';
  var items = state.view === 'overview' ? D.parts : D.extracts;
  var wrapEl = document.createElement('div'); wrapEl.className = 'partcards';
  items.forEach(function (it) {
    var b = document.createElement('button'); b.className = 'pc' + ((state.view === 'overview' ? !it.live : !it.live) ? ' soon' : '');
    if (state.view === 'overview') {
      b.innerHTML = '<b>Part ' + esc(it.id) + ' · ' + esc(it.title) + '</b><span>' + it.count + ' extracts' + (it.live ? '' : ' · coming soon') + '</span>';
      b.onclick = function () { if (it.live) go('part', it.id); else showPart(it); };
    } else {
      var inT = !state.theme || it.themes.indexOf(state.theme) >= 0;
      b.style.opacity = inT ? '' : '.35';
      b.innerHTML = '<b>' + esc(it.id) + ' · ' + esc(it.short) + '</b><span>' + esc(it.author.replace(/[\[\]]/g, '')) + ' · ' + esc(it.year) + '</span>';
      b.onclick = function () { select(it.id); };
    }
    wrapEl.appendChild(b);
  });
  box.appendChild(wrapEl);
}

function crumbs() {
  var c = $('crumbs'); c.innerHTML = '';
  var a = document.createElement('button'); a.textContent = 'The whole book'; a.onclick = function () { go('overview'); };
  c.appendChild(a);
  if (state.view === 'part') {
    var s = document.createElement('span'); s.textContent = '›'; c.appendChild(s);
    var p = document.createElement('span'); p.innerHTML = '<strong>Part I · The art of memory</strong>'; c.appendChild(p);
  }
  var th = $('themes'); th.innerHTML = '';
  th.hidden = state.view !== 'part';
  if (state.view === 'part') {
    var l = document.createElement('span'); l.className = 'lbl'; l.textContent = 'Follow a thread:'; th.appendChild(l);
    D.themes.forEach(function (t) {
      var b = document.createElement('button'); b.className = 'chip' + (state.theme === t.id ? ' on' : ''); b.textContent = t.label;
      b.onclick = function () { state.theme = state.theme === t.id ? null : t.id; render(); };
      th.appendChild(b);
    });
  }
}

function linksFor(e) {
  var out = '<a href="' + D.book.url + '" target="_blank" rel="noopener">Read it in the book<small>Part I, extract ' + esc(e.id) + ', printed pages ' + esc(e.pages) + ' in the Cambridge edition</small></a>';
  out += '<a href="https://archive.org/search?query=' + encodeURIComponent(e.search) + '" target="_blank" rel="noopener">Look for the original<small>Search the Internet Archive for the early printed text</small></a>';
  (e.wiki || []).forEach(function (w) { out += '<a href="' + w[1] + '" target="_blank" rel="noopener">Background: ' + esc(w[0]) + '<small>Wikipedia</small></a>'; });
  return out;
}

function panelExtract(e) {
  var p = $('panel');
  var i = D.extracts.indexOf(e), prev = D.extracts[i - 1], next = D.extracts[i + 1];
  var h = '<div class="pnum">Part I · ' + esc(e.id) + ' · pp. ' + esc(e.pages) + '</div><h2>' + esc(e.short) + '</h2><div class="who">' + esc(e.author.replace(/[\[\]]/g, '')) + ' · ' + esc(e.year) + '</div>';
  if (e.live) {
    h += '<p class="essence">' + esc(e.essence) + '</p><h3>What it says</h3><ul>' + e.points.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>';
    h += '<h3>Picture it</h3><div class="box2">' + esc(e.picture) + '</div><h3>Try it yourself</h3><div class="box2">' + esc(e.tryit) + '</div>';
    if (e.note) h += '<h3>A note from the margin</h3><div class="box2 margin">' + esc(e.note) + '</div>';
    h += '<h3>Threads</h3><div class="pills">' + e.themes.map(function (t) { return '<button class="pill" data-t="' + t + '">' + esc(themeLabel(t)) + '</button>'; }).join('') + '</div>';
  } else {
    h += '<p class="essence">The summary of this extract is on its way. In the meantime you can find it in the book or look for the original.</p>';
  }
  h += '<h3>Go to the book</h3><div class="links">' + linksFor(e) + '</div>';
  h += '<div class="navrow"><button ' + (prev ? 'data-go="' + prev.id + '"' : 'disabled style="opacity:.3"') + '>← ' + (prev ? esc(prev.id) : '') + '</button><button ' + (next ? 'data-go="' + next.id + '"' : 'disabled style="opacity:.3"') + '>' + (next ? esc(next.id) : '') + ' →</button></div>';
  p.innerHTML = h;
  p.querySelectorAll('[data-go]').forEach(function (b) { b.onclick = function () { select(b.getAttribute('data-go')); }; });
  p.querySelectorAll('.pill').forEach(function (b) { b.onclick = function () { state.theme = b.getAttribute('data-t'); render(); }; });
}

function showPart(p) {
  $('panel').innerHTML = '<div class="pnum">Part ' + esc(p.id) + '</div><h2>' + esc(p.title) + '</h2><p class="essence" style="margin-top:8px">' + esc(p.blurb) + '</p><p class="hint">' + p.count + ' extracts. This part is being added soon.</p><div class="links" style="margin-top:14px"><a href="' + D.book.url + '" target="_blank" rel="noopener">Read it in the book<small>' + esc(D.book.publisher) + '</small></a></div>';
}

function panelHome() {
  var h = '<div class="pnum">Start here</div><h2>' + esc(D.book.title) + '</h2><div class="who">' + esc(D.book.subtitle) + ' · ' + esc(D.book.editors) + '</div>';
  if (state.view === 'overview') {
    h += '<p class="essence">An anthology of seventy or so writers from 1500 to 1700, gathered in six parts. Each extract shows how English readers thought about remembering: with imagined buildings, strange pictures, notebooks, prayers and poems.</p><p class="hint">Begin with <strong>Part I</strong>. The others are coming.</p>';
  } else {
    h += '<p class="essence">Ten guides to building a memory. Click a node to see what each one says and how to find it. Then use the threads above to see which books share an idea.</p>';
  }
  h += '<div class="links" style="margin-top:14px"><a href="memory_arts_notes_method.html">My notes: how to build a memory palace<small>the method, step by step, in notebook form</small></a><a href="' + D.book.url + '" target="_blank" rel="noopener">Open the book<small>Cambridge University Press, 2016</small></a></div>';
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

$('booklink').href = D.book.url; $('booklink').textContent = D.book.title + ' (' + D.book.publisher + ')';
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
