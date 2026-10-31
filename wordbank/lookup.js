/* Select a word in a lesson: show its meaning and a picture, and offer to add it to My Words.
   Meanings come from your own My Words bank first, then a free online dictionary.
   Pictures come from your own word pictures first, then Wikipedia for concrete nouns. */
(function () {
  var script = document.currentScript, base = script ? script.src.replace(/lookup\.js.*$/, '') : 'wordbank/';
  var KEY = 'wb_v1', card = null, token = 0, bankLoaded = false, bankWaiting = [];
  var CSS = '.wbl{position:fixed;z-index:100000;width:min(320px,calc(100vw - 20px));background:#1e293b;color:#e8edf5;font:14px/1.45 system-ui,-apple-system,sans-serif;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.35);padding:14px 16px 12px}' +
    '.wbl h4{margin:0 24px 2px 0;font:700 17px/1.2 system-ui,sans-serif;color:#fff}.wbl .p{color:#5eead4;font-size:12px;margin-bottom:8px}' +
    '.wbl img{display:block;width:100%;max-height:150px;object-fit:cover;border-radius:8px;margin:6px 0 8px;background:#0f172a}' +
    '.wbl .d{margin:0 0 6px}.wbl .e{margin:0 0 8px;color:#b6c2d4;font-style:italic}.wbl .s{font-size:11px;color:#8393a8;margin-top:8px}' +
    '.wbl button.a{background:#14b8a6;color:#fff;border:0;border-radius:8px;padding:7px 12px;font:600 13px system-ui,sans-serif;cursor:pointer}' +
    '.wbl button.a[disabled]{background:#334155;color:#cbd5e1;cursor:default}.wbl a{color:#5eead4;margin-left:10px;font-size:13px}' +
    '.wbl .x{position:absolute;top:6px;right:8px;background:none;border:0;color:#94a3b8;font-size:20px;cursor:pointer;line-height:1}';
  var st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function close() { token++; if (card) { card.remove(); card = null; } }
  function clean(t) { t = (t || '').replace(/[‘’]/g, "'").trim(); return /^[A-Za-z][A-Za-z' -]{1,28}[A-Za-z]$/.test(t) && t.split(/\s+/).length <= 3 ? t.toLowerCase() : ''; }
  function stems(w) {
    var o = [w];
    if (/ies$/.test(w)) o.push(w.slice(0, -3) + 'y');
    if (/(es|s)$/.test(w)) { o.push(w.slice(0, -1)); o.push(w.slice(0, -2)); }
    if (/ed$/.test(w)) { o.push(w.slice(0, -2)); o.push(w.slice(0, -1)); }
    if (/ing$/.test(w)) { o.push(w.slice(0, -3)); o.push(w.slice(0, -3) + 'e'); }
    if (/ly$/.test(w)) o.push(w.slice(0, -2));
    return o.filter(function (x, i) { return x.length > 1 && o.indexOf(x) === i; });
  }
  function loadBank(cb) {
    if (bankLoaded || window.WORDBANK) { bankLoaded = true; return cb(); }
    bankWaiting.push(cb); if (bankWaiting.length > 1) return;
    var n = 0, done = function () { if (++n === 2) { bankLoaded = true; bankWaiting.splice(0).forEach(function (f) { f(); }); } };
    [base + 'words.js', base + 'pics.js'].forEach(function (u) { var s = document.createElement('script'); s.src = u; s.onload = s.onerror = done; document.head.appendChild(s); });
  }
  function fromBank(w) {
    var W = (window.WORDBANK && window.WORDBANK.words) || {}, c = {};
    try { c = JSON.parse(localStorage.getItem(KEY) || '{}').custom || {}; } catch (e) {}
    var hit = stems(w).map(function (x) { return W[x] || c[x]; }).filter(Boolean)[0];
    if (!hit || !(hit.def || hit.ex)) return null;
    var key = (window.WORD_PICS || {})[hit.w];
    return { word: hit.w, pos: hit.pos || '', def: hit.def || '', ex: hit.ex || '', img: key ? base + 'pics/' + key + '.png' : '', src: 'My Words' };
  }
  function getJSON(url) { return fetch(url).then(function (r) { if (!r.ok) throw 0; return r.json(); }); }
  function dict(w) {
    var list = stems(w), i = 0;
    return (function next() {
      if (i >= list.length) return Promise.reject();
      var x = list[i++];
      return getJSON('https://api.dictionaryapi.dev/api/v2/entries/en/' + encodeURIComponent(x)).then(function (j) {
        var m = j[0].meanings[0], d = m.definitions[0], ex = '';
        j[0].meanings.forEach(function (mm) { mm.definitions.forEach(function (dd) { if (!ex && dd.example) ex = dd.example; }); });
        return { word: j[0].word, pos: m.partOfSpeech, def: d.definition, ex: ex, noun: m.partOfSpeech === 'noun', src: 'dictionaryapi.dev (Wiktionary)' };
      }).catch(next);
    })();
  }
  function wiki(w) {
    return getJSON('https://en.wikipedia.org/api/rest_v1/page/summary/' + encodeURIComponent(w)).then(function (j) {
      var t = (j.title || '').toLowerCase();
      if (j.type !== 'standard' || !j.thumbnail || !(t === w || t.indexOf(w) > -1 || w.indexOf(t) > -1)) throw 0;
      return j.thumbnail.source;
    });
  }
  function place(rect) {
    var w = card.offsetWidth, h = card.offsetHeight, vw = window.innerWidth, vh = window.innerHeight;
    var x = Math.min(Math.max(10, rect.left + rect.width / 2 - w / 2), vw - w - 10);
    var y = rect.bottom + 10; if (y + h > vh - 10) y = Math.max(10, rect.top - h - 10);
    card.style.left = x + 'px'; card.style.top = y + 'px';
  }
  function add(r) {
    try {
      var d = JSON.parse(localStorage.getItem(KEY) || '{}'); d.custom = d.custom || {};
      d.custom[r.word] = { w: r.word, pos: r.pos || '', def: r.def || '', ex: r.ex || '' };
      localStorage.setItem(KEY, JSON.stringify(d)); return true;
    } catch (e) { return false; }
  }
  function show(word, rect) {
    close(); var me = token;
    card = document.createElement('div'); card.className = 'wbl'; card.setAttribute('role', 'dialog'); card.setAttribute('aria-label', 'Meaning of ' + word);
    card.innerHTML = '<button class="x" aria-label="Close">×</button><h4>' + esc(word) + '</h4><div class="d">Looking it up…</div>';
    card.querySelector('.x').onclick = close; document.body.appendChild(card); place(rect);
    loadBank(function () {
      if (me !== token) return;
      var b = fromBank(word), p = b ? Promise.resolve(b) : dict(word);
      p.then(function (r) {
        if (me !== token) return;
        var src = r.src, imgSrc = '';
        var html = '<button class="x" aria-label="Close">×</button><h4>' + esc(r.word) + '</h4>' + (r.pos ? '<div class="p">' + esc(r.pos) + '</div>' : '') +
          '<div id="wblimg"></div>' + (r.def ? '<p class="d">' + esc(r.def) + '</p>' : '') + (r.ex ? '<p class="e">“' + esc(r.ex) + '”</p>' : '') +
          '<button class="a">Add to My Words</button><a href="' + base + 'index.html#add" target="_blank" rel="noopener" style="display:none" id="wblopen">Open My Words</a>' +
          '<div class="s">Meaning: ' + esc(src) + '<span id="wblpic"></span></div>';
        card.innerHTML = html; card.querySelector('.x').onclick = close;
        var btn = card.querySelector('.a');
        btn.onclick = function () { if (add(r)) { btn.textContent = 'Added ✓'; btn.disabled = true; card.querySelector('#wblopen').style.display = ''; } else btn.textContent = 'Could not save'; };
        place(rect);
        function pic(u, who) {
          if (me !== token || !card) return; var im = new Image(); im.alt = '';
          im.onload = function () { if (me !== token || !card) return; card.querySelector('#wblimg').appendChild(im); card.querySelector('#wblpic').textContent = ' · Picture: ' + who; place(rect); };
          im.src = u;
        }
        if (r.img) pic(r.img, 'My Words'); else if (r.noun) wiki(r.word).then(function (u) { pic(u, 'Wikipedia'); }).catch(function () {});
      }).catch(function () {
        if (me !== token || !card) return;
        card.querySelector('.d').textContent = 'No meaning found for “' + word + '”. Try one word at a time.'; place(rect);
      });
    });
  }
  function onSelect(ev) {
    setTimeout(function () {
      if (card && card.contains(ev.target)) return;
      var s = window.getSelection(); if (!s || s.isCollapsed || !s.rangeCount) return;
      var node = s.anchorNode && (s.anchorNode.nodeType === 3 ? s.anchorNode.parentElement : s.anchorNode);
      if (!node || node.closest('input,textarea,select,button,[contenteditable="true"],.wbl')) return;
      var w = clean(s.toString()); if (!w) return;
      show(w, s.getRangeAt(0).getBoundingClientRect());
    }, 15);
  }
  document.addEventListener('mouseup', onSelect);
  document.addEventListener('touchend', onSelect);
  document.addEventListener('mousedown', function (e) { if (card && !card.contains(e.target)) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
})();
