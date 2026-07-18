#!/usr/bin/env python3
"""Rebuild the role-play finder.

Reads the three role-play dashboards and every rp_/ml_/wk_ lesson file, pulls
out each lesson's situation, skill and ten phrases, and writes
roleplay_finder.html with the data baked in (so it works from file:// and needs
no server).

Run it after adding lessons:   python3 build_roleplay_finder.py
"""

import json
import re
from pathlib import Path

HERE = Path(__file__).parent

DASHBOARDS = [
    ("everyday_echoes_dashboard.html", "Everyday Echoes", "🎭"),
    ("modern_life_dashboard.html", "Modern Life", "💡"),
    ("english_at_work_dashboard.html", "English at Work", "💼"),
]

CARD_RE = re.compile(
    r'<a class="lcard" href="([^"]+)".*?'
    r'<div class="lt">(.*?)</div><div class="ld">(.*?)</div>'
    r'(?:<span class="lg">(.*?)</span>)?',
    re.S,
)


def clean(s):
    """Strip tags and unescape the handful of entities we actually use."""
    s = re.sub(r"<[^>]+>", "", s or "")
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&nbsp;", " "), ("&#39;", "'"), ("&quot;", '"')):
        s = s.replace(a, b)
    return s.strip()


def phrases_from(path):
    """The ten taught phrases live as the <b> opener of each .rev in panel p2."""
    try:
        html = path.read_text(encoding="utf-8")
    except OSError:
        return []
    panel = re.search(r'id="p2"(.*?)id="p3"', html, re.S)
    if not panel:
        return []
    out = []
    for raw in re.findall(r'<div class="rev">\s*<b>(.*?)</b>', panel.group(1), re.S):
        p = clean(raw)
        p = re.sub(r"^[A-C]\s*[—-]\s*", "", p)   # "B — "
        p = re.sub(r"^e\.g\.\s*", "", p)          # "e.g. "
        p = p.strip().strip('"').strip()
        if p:
            out.append(p)
    return out


def collect():
    lessons = []
    for dash, series, emoji in DASHBOARDS:
        dpath = HERE / dash
        if not dpath.exists():
            print(f"  ! missing dashboard {dash}, skipping")
            continue
        for href, title, desc, skill in CARD_RE.findall(dpath.read_text(encoding="utf-8")):
            for level, fname in (("B2/C1", href), ("A2/B1", href.replace(".html", "_a2b1.html"))):
                fpath = HERE / fname
                if not fpath.exists():
                    continue
                ph = phrases_from(fpath)
                if not ph:
                    print(f"  ! no phrases found in {fname}")
                lessons.append({
                    "file": fname,
                    "title": clean(title),
                    "desc": clean(desc),
                    "skill": clean(skill),
                    "series": series,
                    "emoji": emoji,
                    "level": level,
                    "phrases": ph,
                })
    return lessons


PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Find the Conversation | Role Plays</title>
<style>
:root{--ink:#2b2a26;--soft:#6f685d;--warm:#faf7f0;--line:#e6ded0;--gold:#b8863b;--gold-d:#8a6329;--card:#fff}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;background:var(--warm);color:var(--ink);line-height:1.6;padding:0 0 60px}
.wrap{max-width:900px;margin:0 auto;padding:0 20px}
header{background:linear-gradient(150deg,#2a5040,#1e3a2f);color:#fff;padding:44px 0 38px;margin-bottom:26px}
header h1{font-size:2rem;font-weight:700;margin-bottom:8px}
header p{opacity:.85;max-width:620px}
.searchbox{position:sticky;top:0;background:var(--warm);padding:16px 0;z-index:5;border-bottom:1px solid var(--line)}
#q{width:100%;padding:15px 18px;font-size:1.05rem;border:2px solid var(--line);border-radius:12px;background:var(--card);color:var(--ink);font-family:inherit}
#q:focus{outline:none;border-color:var(--gold)}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.chip{padding:6px 14px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--soft);cursor:pointer;font-size:.85rem;font-family:inherit}
.chip.on{background:var(--gold);border-color:var(--gold);color:#fff;font-weight:600}
.count{color:var(--soft);font-size:.9rem;margin:18px 0 10px}
.lesson{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px 22px;margin-bottom:14px}
.lhead{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:4px}
.lhead a{color:var(--ink);text-decoration:none;font-weight:700;font-size:1.15rem}
.lhead a:hover{color:var(--gold-d)}
.tag{font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;color:var(--gold-d);background:#f6efe2;padding:3px 9px;border-radius:999px}
.tag.lvl{color:var(--soft);background:#f0ede6}
.ld{color:var(--soft);font-size:.95rem;margin-bottom:10px}
.hits{border-top:1px dashed var(--line);padding-top:10px;margin-top:10px}
.hit{font-size:.92rem;padding:3px 0;color:#43403a}
.hit:before{content:"“";color:var(--gold)}
.hit:after{content:"”";color:var(--gold)}
mark{background:#ffe9a8;color:inherit;padding:0 1px;border-radius:2px}
.none{text-align:center;color:var(--soft);padding:50px 20px}
.back{display:block;text-align:center;margin-top:26px;color:var(--gold-d);text-decoration:none;font-weight:600}
footer{text-align:center;color:var(--soft);font-size:.85rem;margin-top:30px}
</style>
</head>
<body>
<header><div class="wrap">
  <h1>Find the conversation</h1>
  <p>Search every role play by the situation you're in, the thing you need to do, or the words you're looking for. Try <em>say no</em>, <em>money</em>, <em>neighbour</em>, <em>apolog</em>, or <em>boss</em>.</p>
</div></header>

<div class="wrap">
  <div class="searchbox">
    <input id="q" type="search" placeholder="What do you need to say?" autocomplete="off" autofocus>
    <div class="filters" id="filters"></div>
  </div>
  <div class="count" id="count"></div>
  <div id="results"></div>
  <a class="back" href="everyday_echoes_dashboard.html">← Back to the role plays</a>
  <footer>__N__ role plays · __P__ phrases</footer>
</div>

<script>
const DATA = __DATA__;
const SERIES = [...new Set(DATA.map(d => d.series))];
const LEVELS = [...new Set(DATA.map(d => d.level))].sort();
let fSeries = null, fLevel = null;

const esc = s => s.replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const words = s => (s.toLowerCase().match(/[a-z0-9']+/g) || []);
// A query word matches any word that STARTS with it, so "say" finds "saying"
// and "apolog" finds "apologise". All query words must match somewhere.
const matches = (text, toks) => { const w = words(text); return toks.every(t => w.some(x => x.startsWith(t))); };
const hl = (s, toks) => {
  let out = esc(s);
  if (!toks.length) return out;
  const pat = toks.map(t => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
  return out.replace(new RegExp('\\b(' + pat + ')[a-z\']*', 'gi'), '<mark>$&</mark>');
};

function chips() {
  const box = document.getElementById('filters');
  box.innerHTML = '';
  const add = (label, on, fn) => {
    const b = document.createElement('button');
    b.className = 'chip' + (on ? ' on' : '');
    b.textContent = label;
    b.onclick = fn;
    box.appendChild(b);
  };
  add('All series', !fSeries, () => { fSeries = null; render(); });
  SERIES.forEach(s => add(s, fSeries === s, () => { fSeries = fSeries === s ? null : s; render(); }));
  LEVELS.forEach(l => add(l, fLevel === l, () => { fLevel = fLevel === l ? null : l; render(); }));
}

function render() {
  const q = document.getElementById('q').value.trim();
  const toks = words(q);
  const out = document.getElementById('results');
  chips();
  let shown = 0;
  out.innerHTML = '';

  DATA.filter(d => (!fSeries || d.series === fSeries) && (!fLevel || d.level === fLevel))
      .map(d => {
        if (!toks.length) return { d, hits: [], score: 0 };
        const inTitle = matches(d.title, toks);
        const inAbout = matches(d.title + ' ' + d.desc + ' ' + d.skill, toks);
                const hits = d.phrases.filter(p => matches(p, toks));
        if (!inAbout && !hits.length) return null;
        return { d, hits, score: (inTitle ? 1000 : 0) + (inAbout ? 100 : 0) + hits.length * 10 };
      })
      .filter(Boolean)
      .sort((a, b) => b.score - a.score)
      .forEach(({ d, hits }) => {
        shown++;
        const el = document.createElement('div');
        el.className = 'lesson';
        el.innerHTML =
          '<div class="lhead"><a href="' + d.file + '">' + d.emoji + ' ' + hl(d.title, toks) + '</a>' +
          '<span class="tag">' + esc(d.skill || d.series) + '</span>' +
          '<span class="tag lvl">' + esc(d.level) + '</span></div>' +
          '<div class="ld">' + hl(d.desc, toks) + '</div>' +
          (hits.length ? '<div class="hits">' + hits.map(p => '<div class="hit">' + hl(p, toks) + '</div>').join('') + '</div>' : '');
        out.appendChild(el);
      });

  document.getElementById('count').textContent =
    shown + (shown === 1 ? ' role play' : ' role plays') + (toks.length ? ' matching “' + q + '”' : '');
  if (!shown) out.innerHTML = '<div class="none">Nothing matches that yet.<br>Try a plainer word — <em>sorry</em>, <em>no</em>, <em>money</em>, <em>late</em>.</div>';
}

document.getElementById('q').addEventListener('input', render);
render();
</script>
</body>
</html>
"""


def main():
    lessons = collect()
    total_phrases = sum(len(l["phrases"]) for l in lessons)
    page = (PAGE
            .replace("__DATA__", json.dumps(lessons, ensure_ascii=False))
            .replace("__N__", str(len(lessons)))
            .replace("__P__", str(total_phrases)))
    out = HERE / "roleplay_finder.html"
    out.write_text(page, encoding="utf-8")
    print(f"Wrote {out.name}: {len(lessons)} role plays, {total_phrases} phrases")
    for series in {l["series"] for l in lessons}:
        n = sum(1 for l in lessons if l["series"] == series)
        print(f"  {series}: {n}")


if __name__ == "__main__":
    main()
