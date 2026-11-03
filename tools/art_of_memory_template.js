(function () {
  var store = null;
  try { var t = '__aom'; window.localStorage.setItem(t, t); window.localStorage.removeItem(t); store = window.localStorage; } catch (e) { store = null; }
  function sget(k) { try { return store ? store.getItem(k) : null; } catch (e) { return null; } }
  function sset(k, v) { try { if (store) store.setItem(k, v); } catch (e) {} }
  var LESSON = document.body.getAttribute('data-lesson') || 'x';

  function norm(s) {
    return (s || '').toLowerCase().replace(/[’']/g, '').replace(/[^a-z0-9À-ſ ]+/g, ' ').replace(/\s+/g, ' ').trim();
  }
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  /* ---------- tabs ---------- */
  window.showTab = function (i, noScroll) {
    var panels = $all('.tab-content'), btns = $all('.tab-btn');
    panels.forEach(function (p, k) { p.classList.toggle('active', k === i); });
    btns.forEach(function (b, k) { b.classList.toggle('active', k === i); b.setAttribute('aria-selected', k === i ? 'true' : 'false'); });
    if (!noScroll) { var nav = $('.tab-nav'); if (nav) nav.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    sset('aom_tab_' + LESSON, String(i));
  };

  /* ---------- timers ---------- */
  var timers = [];
  function fmt(s) { var m = Math.floor(s / 60), r = s % 60; return m + ':' + (r < 10 ? '0' : '') + r; }
  function runTimer(box, secs, onTick, onEnd) {
    var disp = $('.timer', box), left = secs, id;
    if (box._id) clearInterval(box._id);
    function paint() {
      disp.textContent = fmt(left);
      disp.classList.toggle('warn', left <= Math.max(10, secs * 0.25) && left > Math.max(5, secs * 0.1));
      disp.classList.toggle('low', left <= Math.max(5, secs * 0.1));
      if (onTick) onTick(left);
    }
    paint();
    id = setInterval(function () {
      left -= 1; paint();
      if (left <= 0) { clearInterval(id); box._id = null; disp.classList.remove('warn'); if (onEnd) onEnd(); }
    }, 1000);
    box._id = id;
    timers.push(id);
  }

  /* ---------- generic click handling ---------- */
  document.addEventListener('click', function (e) {
    var t = e.target;
    var btn = t.closest ? t.closest('button, .fcard, a') : null;
    if (!btn) return;

    if (btn.classList.contains('reveal-btn')) {
      var r = btn.nextElementSibling;
      if (r) { r.classList.toggle('show'); }
      return;
    }
    if (btn.classList.contains('w')) { btn.parentElement.classList.toggle('open'); return; }

    var act = btn.getAttribute('data-act');
    if (!act) return;
    var ex = btn.closest('.ex, .recall, .card-deck') || document;

    if (act === 'gap') {
      var ok = 0, all = $all('.gapin', ex);
      all.forEach(function (inp) {
        var accepted = (inp.getAttribute('data-ans') || '').split('|').map(norm);
        var v = norm(inp.value);
        var good = v && accepted.indexOf(v) > -1;
        inp.classList.toggle('ok', !!good); inp.classList.toggle('no', !good);
        var note = inp.parentElement.querySelector('.gapans[data-for="' + inp.id + '"]');
        if (note) { note.textContent = good ? '' : '→ ' + inp.getAttribute('data-ans').split('|')[0]; }
        if (good) ok++;
      });
      var fb = $('.fb', ex);
      fb.className = 'fb ' + (ok === all.length ? 'ok' : 'no');
      fb.textContent = ok === all.length ? 'All ' + all.length + ' correct.' : ok + ' of ' + all.length + ' correct. The answers you missed are shown in red; fix them, then check again.';
      return;
    }
    if (act === 'mc') {
      var q = btn.closest('.ex');
      var good = btn.getAttribute('data-ok') === '1';
      var fb2 = $('.fb', q);
      $all('.mc-opt', q).forEach(function (o) { if (o !== btn && !o.classList.contains('ok')) { o.classList.remove('no'); } });
      btn.classList.add(good ? 'ok' : 'no');
      fb2.className = 'fb ' + (good ? 'ok' : 'no');
      fb2.innerHTML = good ? (q.getAttribute('data-why') || 'Correct.') : (btn.getAttribute('data-hint') || 'Not quite. Think again and try another answer.');
      return;
    }
    if (act === 'match') {
      var okm = 0, rows = $all('.match-row', ex);
      rows.forEach(function (row) {
        var sel = $('select', row), good = sel.value === sel.getAttribute('data-ans');
        row.classList.toggle('ok', good); row.classList.toggle('no', !good && sel.value !== '');
        if (good) okm++;
      });
      var fb3 = $('.fb', ex);
      fb3.className = 'fb ' + (okm === rows.length ? 'ok' : 'no');
      fb3.textContent = okm === rows.length ? 'All ' + rows.length + ' matched.' : okm + ' of ' + rows.length + ' matched. Change the red ones and check again.';
      return;
    }
    if (act === 'timer') {
      var box = btn.closest('.timer-box'), secs = parseInt(box.getAttribute('data-secs'), 10) || 60;
      var msg = $('.timer-msg', box);
      if (msg) msg.textContent = '';
      runTimer(box, secs, null, function () { if (msg) msg.textContent = 'Time is up.'; });
      return;
    }
    if (act === 'timer-reset') {
      var b2 = btn.closest('.timer-box'); if (b2._id) clearInterval(b2._id);
      $('.timer', b2).textContent = fmt(parseInt(b2.getAttribute('data-secs'), 10) || 60);
      $('.timer', b2).className = 'timer';
      return;
    }
    if (act === 'flip') { return; }
    if (act === 'next' || act === 'prev' || act === 'shuffle') {
      var deck = btn.closest('.card-deck');
      var cards = JSON.parse(deck.getAttribute('data-cards'));
      var i = parseInt(deck.getAttribute('data-i'), 10) || 0;
      if (act === 'shuffle') { cards.sort(function () { return Math.random() - 0.5; }); deck.setAttribute('data-cards', JSON.stringify(cards)); i = 0; }
      else if (act === 'next') i = (i + 1) % cards.length; else i = (i - 1 + cards.length) % cards.length;
      deck.setAttribute('data-i', i); paintCard(deck); return;
    }
    if (act === 'rc-start') { startRecall(btn.closest('.recall')); return; }
    if (act === 'rc-ready') { endStudy(btn.closest('.recall')); return; }
    if (act === 'rc-check') { checkRecall(btn.closest('.recall')); return; }
    if (act === 'rc-again') { resetRecall(btn.closest('.recall')); return; }
    if (act === 'done') {
      sset('aom_done_' + LESSON, '1');
      btn.textContent = 'Marked as done ✓';
      return;
    }
  });

  /* flash cards */
  function paintCard(deck) {
    var cards = JSON.parse(deck.getAttribute('data-cards')), i = parseInt(deck.getAttribute('data-i'), 10) || 0;
    var c = cards[i], el = $('.fcard', deck);
    el.classList.remove('flip');
    $('.front', el).innerHTML = c[0]; $('.back', el).innerHTML = c[1];
    $('.cnt', deck).textContent = (i + 1) + ' of ' + cards.length;
  }
  document.addEventListener('click', function (e) {
    var f = e.target.closest ? e.target.closest('.fcard') : null;
    if (f) f.classList.toggle('flip');
  });
  $all('.card-deck').forEach(paintCard);

  /* memory challenge */
  function stage(rc, name) { $all('.stage', rc).forEach(function (s) { s.classList.toggle('on', s.getAttribute('data-stage') === name); }); }
  function startRecall(rc) {
    var items = JSON.parse(rc.getAttribute('data-items')), ordered = rc.getAttribute('data-ordered') === '1';
    var wrap = $('.items', rc); wrap.className = 'items' + (ordered ? ' ordered' : '');
    wrap.innerHTML = '';
    items.forEach(function (it) { var s = document.createElement('span'); s.textContent = it.split('|')[0]; wrap.appendChild(s); });
    stage(rc, 'study');
    var box = $('.timer-box', rc), secs = parseInt(rc.getAttribute('data-secs'), 10) || 60;
    box.setAttribute('data-secs', secs);
    runTimer(box, secs, null, function () { endStudy(rc); });
  }
  function endStudy(rc) {
    var box = $('.timer-box', rc); if (box._id) { clearInterval(box._id); box._id = null; }
    $('.items', rc).innerHTML = '';
    stage(rc, 'recall');
    var ta = $('textarea', rc); ta.value = ''; ta.focus();
  }
  function checkRecall(rc) {
    var items = JSON.parse(rc.getAttribute('data-items')), ordered = rc.getAttribute('data-ordered') === '1';
    var raw = $('textarea', rc).value, text = norm(raw);
    var lines = raw.split(/\n+/).map(norm).filter(Boolean);
    var res = $('.res', rc), got = 0; res.innerHTML = '';
    items.forEach(function (it, i) {
      var alts = it.split('|').map(norm), good = false;
      if (ordered) {
        var ln = lines[i] || '';
        good = alts.some(function (a) { return ln && (ln.indexOf(a) > -1 || (ln.length >= 4 && a.indexOf(ln) > -1)); });
      } else {
        var padded = ' ' + text + ' ';
        good = alts.some(function (a) { return padded.indexOf(' ' + a + ' ') > -1 || padded.indexOf(a) > -1; });
      }
      if (good) got++;
      var d = document.createElement('div'); d.className = good ? 'ok' : 'no';
      d.textContent = (ordered ? (i + 1) + '. ' : '') + it.split('|')[0] + (good ? '  ✓' : '  ✗');
      res.appendChild(d);
    });
    $('.score', rc).textContent = got + ' of ' + items.length + ' recalled';
    stage(rc, 'result');
  }
  function resetRecall(rc) { stage(rc, 'start'); }

  /* build-it self checks */
  document.addEventListener('change', function (e) {
    var cb = e.target;
    if (cb.type === 'checkbox' && cb.closest('.checks')) {
      var box = cb.closest('.ex'), all = $all('.checks input', box), done = all.every(function (c) { return c.checked; });
      var fb = $('.fb', box);
      if (fb) { fb.className = done ? 'fb ok' : 'fb'; if (done) fb.textContent = 'Every box ticked: each of those is a reason the picture will still be there tomorrow.'; }
    }
    if (cb.type === 'checkbox' && cb.hasAttribute('data-save')) { sset('aom_' + LESSON + '_' + cb.getAttribute('data-save'), cb.checked ? '1' : '0'); }
  });

  /* saved text / ticks */
  $all('textarea[data-save]').forEach(function (ta) {
    var k = 'aom_' + LESSON + '_' + ta.getAttribute('data-save'), v = sget(k);
    if (v) ta.value = v;
    ta.addEventListener('input', function () { sset(k, ta.value); });
  });
  $all('input[type=checkbox][data-save]').forEach(function (cb) {
    if (sget('aom_' + LESSON + '_' + cb.getAttribute('data-save')) === '1') cb.checked = true;
  });
  if (sget('aom_done_' + LESSON) === '1') { var d = $('[data-act=done]'); if (d) d.textContent = 'Marked as done ✓'; }

  /* hub progress */
  $all('[data-room]').forEach(function (el) {
    if (sget('aom_done_' + el.getAttribute('data-room')) === '1') el.classList.add('done');
  });
  /* open on a remembered tab only when asked by hash */
  var tabNames = ['story', 'method', 'try', 'drill', 'back'];
  var h = (location.hash || '').replace('#', ''), hi = tabNames.indexOf(h);
  if ($('.tab-nav')) showTab(hi > -1 ? hi : 0, true);
})();
