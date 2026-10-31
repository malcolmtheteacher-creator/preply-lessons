(function () {
  var script = document.currentScript, base = script ? script.src.replace(/hook\.js.*$/, '') : 'wordbank/';
  var isDash = !!(script && script.getAttribute('data-page') === 'dashboard');
  var id = location.pathname.split('/').pop().replace(/\.html$/, ''); try { id = decodeURIComponent(id); } catch (e) {}

  function remember() {
    try {
      var k = 'wb_v1', d = JSON.parse(localStorage.getItem(k) || '{}');
      d.done = d.done || {};
      if (!d.done[id]) d.done[id] = Date.now();
      d.latest = id;
      localStorage.setItem(k, JSON.stringify(d));
    } catch (e) {}
  }
  function link(href, text, css) {
    var a = document.createElement('a');
    a.href = href; a.target = '_blank'; a.rel = 'noopener'; a.textContent = text; a.style.cssText = css;
    return a;
  }
  function bar(n) {
    var b = document.createElement('div');
    b.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:99999;background:#1e293b;color:#e8edf5;font:14px/1.4 system-ui,-apple-system,sans-serif;padding:9px 14px;display:flex;gap:12px;align-items:center;justify-content:center;flex-wrap:wrap;box-shadow:0 -2px 10px rgba(0,0,0,.25)';
    var t = document.createElement('span');
    t.textContent = isDash ? 'Your vocabulary from every lesson lives in My Words.'
      : n ? n + ' words from this lesson are saved in My Words.' : 'This lesson is saved in My Room.';
    b.appendChild(t);
    if (n || isDash) {
      b.appendChild(link(base + 'index.html' + (isDash ? '' : '?lesson=' + encodeURIComponent(id)),
        isDash ? 'Open My Words' : 'Practise them',
        'background:#14b8a6;color:#fff;text-decoration:none;padding:6px 14px;border-radius:8px;font-weight:600;white-space:nowrap'));
      b.appendChild(link(base + 'index.html#add', '+ Add a word', 'color:#5eead4;text-decoration:none;white-space:nowrap'));
      b.appendChild(link(base + '../journey/index.html', 'My Room', 'color:#fcd34d;text-decoration:none;white-space:nowrap'));
    } else {
      b.appendChild(link(base + '../journey/index.html', 'Open My Room',
        'background:#d4a017;color:#1e293b;text-decoration:none;padding:6px 14px;border-radius:8px;font-weight:600;white-space:nowrap'));
    }
    var x = document.createElement('button');
    x.textContent = '\u00d7'; x.setAttribute('aria-label', 'Hide');
    x.style.cssText = 'background:none;border:0;color:#94a3b8;font-size:20px;cursor:pointer';
    x.onclick = function () { b.remove(); };
    b.appendChild(x);
    document.body.appendChild(b);
    document.body.style.paddingBottom = '64px';
  }
  function go() {
    var s = document.createElement('script');
    s.src = base + 'lessons.js';
    s.onload = function () {
      var n = (window.WBLESSONS || {})[id] || 0;
      if (isDash) return bar(0);
      remember(); bar(n);
      var l = document.createElement('script'); l.src = base + 'lookup.js'; document.head.appendChild(l);
    };
    document.head.appendChild(s);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();
