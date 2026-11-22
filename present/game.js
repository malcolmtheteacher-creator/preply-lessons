// Atlas of Empires - what each player sees.
(() => {
  const $ = s => document.querySelector(s), el = (t, c, h) => { const e = document.createElement(t); if (c) e.className = c; if (h != null) e.innerHTML = h; return e; };
  const NS = 'http://www.w3.org/2000/svg', sv = (t, a) => { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); return e; };
  const LANDS = MAP.lands, L = Object.fromEntries(LANDS.map(t => [t.id, t])), REG = MAP.regions;
  const COLORS = ['crimson', 'navy', 'forest', 'gold', 'plum', 'ink'];
  const cls = c => c === 'gold' ? 'gold-c' : c === 'ink' ? 'ink-c' : c;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const store = { get: k => { try { return localStorage.getItem(k) || ''; } catch (e) { return ''; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) { } } };
  const qs = new URLSearchParams(location.search);
  const SEAT = qs.get('seat') || '';                    // lets one Mac open several seats for testing
  let pid = store.get('aoe_pid' + SEAT);
  let S = null, sel = null, perClick = 1, tint = true, lastSeq = -1, held = null, battleOpen = null, chosen = new Set(), amountCb = null, lookAtBoard = false, bookAt = 0, firstBoard = true;

  // ------------------------------------------------------------ talking to the host
  const SHOW = !!window.SHOWROOM;      // the present on the website: unwrap it and look round; no host Mac needed
  function showState(stage) {
    const players = ['Crimson', 'Navy', 'Forest', 'Gold', 'Plum', 'Black'].map((n, i) => ({ k: 'k' + i, name: n + ' Army', color: COLORS[i], bot: false, host: false, out: false, spare: 0, cards: i % 3, on: true, cam: false, lands: 0, armies: 0, income: 3 }));
    let seed = 20261122; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    const ids = LANDS.map(t => t.id), lands = {}; for (let i = ids.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [ids[i], ids[j]] = [ids[j], ids[i]]; }
    ids.forEach((id, k) => { lands[id] = { o: k % 6, n: 1 + Math.floor(rnd() * rnd() * 11) }; });
    players.forEach((p, i) => { const mine = ids.filter(id => lands[id].o === i); p.lands = mine.length; p.armies = mine.reduce((t, id) => t + lands[id].n, 0); p.income = Math.max(3, Math.floor(mine.length / 3)); });
    return { v: 1, stage, me: -1, opts: { setup: 'place', goal: 'world' }, turn: 0, phase: 'attack', pending: 0, round: 1, sets: 0, nextSet: 4, setupLeft: 0, movein: null, moved: false, mid: false, battle: null, winner: null,
      log: [{ text: 'The lands are dealt and the armies stand ready.' }], deck: 52, goal: 30, lands, inc: { n: 3, lands: 8, regs: [] }, players,
      hand: [{ land: 'british_isles', sym: 'crown' }, { land: 'philippines', sym: 'anchor' }, { land: null, sym: 'wild' }], join: { host: '', ips: [], port: 0, far: '' }, rtc: [] };
  }
  function post(m) {
    if (SHOW) return Promise.resolve({});
    return fetch('/act', { method: 'POST', body: JSON.stringify({ ...m, pid }) }).then(r => r.json()).then(o => { if (o.err) toast(o.err); return o; }).catch(() => toast('The host Mac is not answering.'));
  }
  let pollGen = 0;
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  async function listen() {            // keep asking the host "anything new?"; it answers the moment something changes
    if (SHOW) { document.body.classList.add('show'); return take(showState('lobby')); }
    const gen = ++pollGen; let v = -1;
    while (gen === pollGen) {
      try {
        const r = await fetch('/poll?v=' + v + '&pid=' + encodeURIComponent(pid), { cache: 'no-store' });
        const s = await r.json(); if (gen !== pollGen) return;
        if (s.rtc) for (const n of s.rtc) Faces.note(n.from, n.d);
        if (s.v !== v) { v = s.v; take(s); }
      } catch (e) { await sleep(1500); }
    }
  }
  function take(s) {
    const fresh = s.battle && s.battle.seq !== lastSeq && lastSeq !== -1 && s.stage !== 'lobby';
    if (lastSeq === -1) lastSeq = s.battle ? s.battle.seq : 0;
    if (fresh) {
      lastSeq = s.battle.seq; const first = !held; held = s;
      if (first) { rollDice(s.battle); setTimeout(() => { const h = held; held = null; S = h; settleDice(h.battle); render(); }, 900); }
      return;
    }
    if (held) { held = s; return; }
    S = s; render();
  }
  let toastT; function toast(t) { const e = $('#toast'); e.textContent = t; e.classList.add('show'); clearTimeout(toastT); toastT = setTimeout(() => e.classList.remove('show'), 3200); }


  // ------------------------------------------------------------ faces at the table
  // Picture and sound travel straight between the players' computers; the host only introduces them to each other.
  const Faces = (() => {
    let on = false, stream = null, mic = true, cam = true, sound = true, chain = Promise.resolve(), tick = null, nagged = 0;
    const peers = {}, pend = {}, since = {}, quiet = new Set(), tiles = {};
    const ICE = { iceServers: [{ urls: ['stun:stun.l.google.com:19302', 'stun:stun1.l.google.com:19302'] }, { urls: 'stun:stun.cloudflare.com:3478' }] };
    const sig = (to, d) => fetch('/act', { method: 'POST', body: JSON.stringify({ t: 'rtc', to, d, pid }) }).catch(() => { });
    const meK = () => S && S.players[S.me] ? S.players[S.me].k : null;
    const fake = () => {              // a moving test picture, for checking without a camera (?fakecam=1)
      const c = document.createElement('canvas'); c.width = 320; c.height = 240; const x = c.getContext('2d'); let t = 0; const hue = Math.floor(Math.random() * 360);
      setInterval(() => { t++; x.fillStyle = `hsl(${hue},45%,22%)`; x.fillRect(0, 0, 320, 240); x.fillStyle = `hsl(${hue},70%,70%)`; x.beginPath(); x.arc(160 + Math.sin(t / 9) * 90, 120 + Math.cos(t / 7) * 50, 36, 0, 7); x.fill(); x.fillStyle = '#fff'; x.font = '22px Georgia'; x.fillText((S && S.players[S.me] ? S.players[S.me].name : '') + ' ' + t, 14, 30); }, 80);
      return c.captureStream(12);
    };
    async function start() {
      if (on) return;
      if (!S || S.me < 0) return toast('Take a seat first, then switch the faces on.');
      if (qs.get('fakecam')) stream = fake();
      else {
        if (!window.isSecureContext || !navigator.mediaDevices) return toast('Faces only work through the far-away link, the one that begins with https. Ask the host for it.');
        const many = S.players.filter(p => !p.bot).length > 4;
        try { stream = await navigator.mediaDevices.getUserMedia({ video: { width: { ideal: many ? 240 : 320 }, height: { ideal: many ? 180 : 240 }, frameRate: { ideal: many ? 12 : 15, max: 20 } }, audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true } }); }
        catch (e) {
          try { stream = await navigator.mediaDevices.getUserMedia({ audio: true }); toast('No camera was found, so the others will hear you but not see you.'); }
          catch (e2) { return toast('The camera and microphone are switched off for this page. Allow them in the browser, then try again.'); }
        }
      }
      on = true; mic = cam = sound = true; post({ t: 'cam', on: true });
      clearInterval(tick); tick = setInterval(sync, 4000); draw(); sync();
    }
    function stop() {
      if (!on) return; on = false; clearInterval(tick);
      for (const k of Object.keys(peers)) drop(k);
      if (stream) for (const t of stream.getTracks()) t.stop(); stream = null;
      post({ t: 'cam', on: false }); draw();
    }
    function drop(k) { const p = peers[k]; if (!p) return; clearTimeout(p.retry); try { p.pc.close(); } catch (e) { } delete peers[k]; }
    function make(k, init) {
      const pc = new RTCPeerConnection(ICE), p = peers[k] = { pc, init, stream: null, state: 'calling', id: init ? Math.random().toString(36).slice(2, 9) : '' };
      for (const t of stream.getTracks()) pc.addTrack(t, stream);
      if (init && !stream.getVideoTracks().length) pc.addTransceiver('video', { direction: 'recvonly' });
      pc.onicecandidate = e => { if (e.candidate) sig(k, { c: e.candidate, id: p.id }); };
      pc.ontrack = e => { p.stream = e.streams[0] || p.stream || new MediaStream(); if (!e.streams[0]) p.stream.addTrack(e.track); draw(); };
      pc.onconnectionstatechange = () => {
        const st = pc.connectionState; p.state = st === 'connected' ? 'live' : st === 'failed' ? 'failed' : st === 'disconnected' ? 'lost' : 'calling'; draw();
        if ((st === 'failed' || st === 'disconnected') && p.init && peers[k] === p) { clearTimeout(p.retry); p.retry = setTimeout(() => { if (peers[k] === p && pc.connectionState !== 'connected') { drop(k); sync(); } }, st === 'failed' ? 3000 : 9000); }
      };
      if (init) (async () => { try { await pc.setLocalDescription(await pc.createOffer()); sig(k, { sdp: pc.localDescription, id: p.id }); } catch (e) { } })();
      return p;
    }
    const note = (from, d) => { chain = chain.then(() => handle(from, d)).catch(() => { }); };
    async function handle(from, d) {
      if (!on) return;
      const flush = async p => { const q = pend[from]; delete pend[from]; if (q && q.id === p.id) for (const c of q.list) await p.pc.addIceCandidate(c).catch(() => { }); };
      if (d.sdp && d.sdp.type === 'offer') {
        drop(from); const p = make(from, false); p.id = d.id;
        await p.pc.setRemoteDescription(d.sdp); await flush(p);
        await p.pc.setLocalDescription(await p.pc.createAnswer()); sig(from, { sdp: p.pc.localDescription, id: p.id }); draw();
      } else if (d.sdp) { const p = peers[from]; if (p && p.id === d.id) { await p.pc.setRemoteDescription(d.sdp); await flush(p); } }
      else if (d.c) {
        const p = peers[from];
        if (p && p.id === d.id && p.pc.remoteDescription) await p.pc.addIceCandidate(d.c).catch(() => { });
        else { if (!pend[from] || pend[from].id !== d.id) pend[from] = { id: d.id, list: [] }; pend[from].list.push(d.c); }
      }
      else if (d.hello) { if (meK() < from) { drop(from); make(from, true); draw(); } }      // the other side has no line to us: call afresh
    }
    function sync() {
      if (!on || !S || S.me < 0) { if (on) draw(); return; }
      const me = meK(), want = new Set(S.players.filter((p, i) => i !== S.me && p.cam && !p.bot).map(p => p.k));
      if (!S.players[S.me].cam && Date.now() - nagged > 5000) { nagged = Date.now(); post({ t: 'cam', on: true }); }     // the host forgot us (a restart): say so again
      for (const k of Object.keys(peers)) if (!want.has(k)) drop(k);
      for (const k of want) {
        if (peers[k]) { delete since[k]; continue; }
        if (me < k) make(k, true);
        else if (!since[k]) since[k] = Date.now();
        else if (Date.now() - since[k] > 3000) { since[k] = Date.now() + 5000; sig(k, { hello: 1 }); }     // nudge the other side to call again
      }
      draw();
    }
    function tile(k) {
      if (tiles[k]) return tiles[k];
      const e = el('div', 'portrait', '<div class="pf"><video autoplay playsinline></video><div class="pwait"></div></div><div class="pname"><span class="seal"></span><b></b></div>');
      e.addEventListener('click', () => { if (k === meK()) return; quiet.has(k) ? quiet.delete(k) : quiet.add(k); draw(); });
      $('#gallery .tiles').appendChild(e); return tiles[k] = { el: e, video: e.querySelector('video') };
    }
    function draw() {
      show('#gallery', on); document.body.classList.toggle('faces', on); fit();
      $('#facesBtn').classList.toggle('on', on); const lb = $('#facesLobby'); lb.classList.toggle('on', on); lb.textContent = on ? 'Hide faces' : 'Show faces';
      if (!on || !S) return;
      const me = meK(), list = S.players.filter(p => !p.bot && (p.k === me || p.cam));
      for (const k of Object.keys(tiles)) if (!list.some(p => p.k === k)) { tiles[k].el.remove(); delete tiles[k]; }
      const room = innerHeight - 150, pw = Math.max(84, Math.min(158, Math.floor(((room / Math.max(1, list.length)) - 34) * 4 / 3)));
      $('#gallery').style.setProperty('--pw', pw + 'px');
      list.forEach((p, i) => {
        const t = tile(p.k), mine = p.k === me, peer = peers[p.k], src = mine ? stream : peer && peer.stream;
        if (t.video.srcObject !== (src || null)) { t.video.srcObject = src || null; if (src) t.video.play().catch(() => { }); }
        t.video.muted = mine || !sound || quiet.has(p.k);
        const turn = S.stage === 'game' && S.players[S.turn] && S.players[S.turn].k === p.k;
        t.el.className = 'portrait ' + cls(p.color) + (mine ? ' mine' : '') + (turn ? ' turn' : '') + (!mine && quiet.has(p.k) ? ' quiet' : '');
        t.el.style.order = i; t.el.title = mine ? 'This is you' : 'Click to turn ' + p.name + "'s sound off or on";
        t.el.querySelector('b').textContent = mine ? p.name + ' (you)' : p.name; t.el.querySelector('.seal').className = 'seal ' + cls(p.color);
        const hasPic = src && src.getVideoTracks().length;
        const st = mine ? (!hasPic ? 'no camera' : cam ? '' : 'camera off') : !peer ? 'calling…' : peer.state === 'live' ? (hasPic ? '' : 'sound only') : peer.state === 'failed' ? 'cannot connect' : peer.state === 'lost' ? 'reconnecting…' : 'calling…';
        const w = t.el.querySelector('.pwait'); w.textContent = st; w.classList.toggle('show', !!st);
      });
      $('#gMic').classList.toggle('off', !mic); $('#gCam').classList.toggle('off', !cam); $('#gSound').classList.toggle('off', !sound);
    }
    const setMic = v => { mic = v; if (stream) for (const t of stream.getAudioTracks()) t.enabled = v; draw(); };
    const setCam = v => { cam = v; if (stream) for (const t of stream.getVideoTracks()) t.enabled = v; draw(); };
    return { start, stop, sync, note, toggle: () => on ? stop() : start(), mic: () => setMic(!mic), cam: () => setCam(!cam), sound: () => { sound = !sound; draw(); }, get on() { return on; }, get peers() { return peers; } };
  })();
  window.__faces = Faces;

  // ------------------------------------------------------------ the board, built once
  const map = $('#map'); map.setAttribute('viewBox', `0 0 ${MAP.W} ${MAP.H}`);
  const defs = sv('defs', {});
  defs.innerHTML = COLORS.map(c => {
    const k = { crimson: ['#f47a82', '#b01f2b', '#5c0d14'], navy: ['#86a6f2', '#22479f', '#0e2152'], forest: ['#74d696', '#1f7d3f', '#0b3d1c'], gold: ['#ffe58e', '#d49a17', '#7a5204'], plum: ['#d795e8', '#7d2f91', '#3c114a'], ink: ['#9c9ca8', '#3a3a44', '#0b0b0e'] }[c];
    return `<radialGradient id="pg-${c}" cx="36%" cy="28%" r="80%"><stop offset="0" stop-color="${k[0]}"/><stop offset=".5" stop-color="${k[1]}"/><stop offset="1" stop-color="${k[2]}"/></radialGradient><linearGradient id="ps-${c}" x1="0" x2="1"><stop offset="0" stop-color="${k[2]}"/><stop offset=".45" stop-color="${k[1]}"/><stop offset="1" stop-color="${k[2]}"/></linearGradient>`;
  }).join('') + '<filter id="psh" x="-60%" y="-60%" width="220%" height="240%"><feGaussianBlur stdDeviation="3.2"/></filter><radialGradient id="pfree" cx="36%" cy="28%" r="80%"><stop offset="0" stop-color="#fff8e0"/><stop offset=".6" stop-color="#d9c79a"/><stop offset="1" stop-color="#8d7a4e"/></radialGradient>';
  map.appendChild(defs);
  const gLand = sv('g', {}), gGlow = sv('g', {}), gFx = sv('g', {}), gPiece = sv('g', {}), gHit = sv('g', {});
  map.append(gLand, gGlow, gFx, gPiece, gHit);
  const N = {};
  for (const t of LANDS) {
    const land = sv('path', { d: t.d, class: 'land', 'fill-rule': 'evenodd' });
    const glow = sv('path', { d: t.d, class: 'glow', 'fill-rule': 'evenodd' });
    const piece = sv('g', { class: 'piece', transform: `translate(${t.x} ${t.y})` });
    const hit = sv('path', { d: t.d, class: 'hit', 'fill-rule': 'evenodd' });
    const spot = sv('circle', { cx: t.x, cy: t.y, r: 30, class: 'hit' });      // the piece itself is always clickable, even on tiny lands
    gLand.appendChild(land); gGlow.appendChild(glow); gPiece.appendChild(piece); gHit.append(hit, spot);
    N[t.id] = { land, glow, piece, hit, spot, n: null, o: null };
    for (const h of [hit, spot]) {
      h.addEventListener('click', () => clickLand(t.id));
      h.addEventListener('mouseenter', () => { hover = t.id; paintGlow(); });
      h.addEventListener('mouseleave', () => { if (hover === t.id) { hover = null; paintGlow(); } });
    }
  }
  let hover = null;

  function drawPiece(id, o, n, color) {
    const p = N[id]; if (p.n === n && p.o === o && p.c === color) return;
    const grew = p.n != null && (p.n !== n || p.o !== o);
    p.n = n; p.o = o; p.c = color;
    const R = 20, stack = n >= 10 ? 3 : n >= 5 ? 2 : 1, c = color || 'free';
    const fillTop = color ? `url(#pg-${c})` : 'url(#pfree)', fillSide = color ? `url(#ps-${c})` : '#7d6c44';
    let h = `<ellipse cx="3" cy="8" rx="${R + 2}" ry="${R * 0.82}" fill="#000" opacity=".5" filter="url(#psh)"/><g class="pop">`;
    for (let k = 0; k < stack; k++) {
      const y = -k * 6;
      h += `<path d="M${-R} ${y} v5.5 a${R} ${R * 0.92} 0 0 0 ${2 * R} 0 v-5.5z" fill="${fillSide}" stroke="rgba(0,0,0,.6)" stroke-width="1"/>` +
        `<ellipse cx="0" cy="${y}" rx="${R}" ry="${R * 0.92}" fill="${fillTop}" stroke="rgba(0,0,0,.55)" stroke-width="1"/>`;
    }
    const ty = -(stack - 1) * 6;
    h += `<ellipse cx="0" cy="${ty}" rx="${R - 4}" ry="${(R - 4) * 0.92}" fill="none" stroke="rgba(255,255,255,.34)" stroke-width="1.2"/>` +
      `<ellipse cx="-6" cy="${ty - 8}" rx="8" ry="4" fill="#fff" opacity=".28" transform="rotate(-24 -6 ${ty - 8})"/>` +
      (n > 0 ? `<text class="num" x="0" y="${ty + 8}">${n}</text>` : '') + '</g>';
    p.piece.innerHTML = h;
    p.piece.setAttribute('class', 'piece ' + (color ? cls(color) : '') + (firstBoard ? ' drop' : grew ? ' bump' : ''));
    if (firstBoard) p.piece.querySelector('.pop').style.animationDelay = (0.25 + Math.random() * 0.9) + 's';
    else if (grew) { void p.piece.getBBox(); }
  }

  // ------------------------------------------------------------ what can be clicked now
  const myTurn = () => S && S.stage === 'game' && S.turn === S.me;
  const mine = id => S.lands[id] && S.lands[id].o === S.me;
  function connected(a, i) { const seen = new Set([a]), q = [a]; while (q.length) { const x = q.shift(); for (const y of L[x].adj) if (!seen.has(y) && S.lands[y].o === i) { seen.add(y); q.push(y); } } return seen; }
  function choices() {
    const can = new Set(), tg = new Set();
    if (!myTurn() || held) return { can, tg };
    const ph = S.phase;
    if (ph === 'claim') { for (const t of LANDS) if (S.lands[t.id].o === -1) can.add(t.id); }
    else if (ph === 'setup' || (ph === 'reinforce' && S.pending > 0 && S.hand.length < 5)) { for (const t of LANDS) if (mine(t.id)) can.add(t.id); }
    else if (ph === 'attack' && !S.movein) {
      for (const t of LANDS) if (mine(t.id) && S.lands[t.id].n >= 2 && t.adj.some(a => !mine(a))) can.add(t.id);
      if (sel && can.has(sel)) for (const a of L[sel].adj) if (!mine(a)) tg.add(a);
    } else if (ph === 'fortify' && !S.moved) {
      for (const t of LANDS) if (mine(t.id) && S.lands[t.id].n >= 2 && t.adj.some(a => mine(a))) can.add(t.id);
      if (sel && can.has(sel)) for (const a of connected(sel, S.me)) if (a !== sel) tg.add(a);
    }
    return { can, tg };
  }
  function paintGlow() {
    if (!S || S.stage === 'lobby') return;
    const { can, tg } = choices();
    for (const t of LANDS) {
      const n = N[t.id]; let c = 'glow';
      if (t.id === sel && (can.has(t.id))) c += ' sel'; else if (tg.has(t.id)) c += ' target'; else if (can.has(t.id)) c += (hover === t.id ? ' can hover' : ' can');
      else if (battleShown && (t.id === battleShown.from || t.id === battleShown.to)) c += ' sel';
      n.glow.setAttribute('class', c);
      const click = can.has(t.id) || tg.has(t.id);
      n.hit.setAttribute('class', 'hit' + (click ? ' click' : '')); n.spot.setAttribute('class', 'hit' + (click ? ' click' : ''));
    }
    gFx.innerHTML = '';
    const ar = battleShown || (sel && hover && tg.has(hover) ? { from: sel, to: hover } : null);
    if (ar) gFx.appendChild(sv('path', { class: 'arrow', d: arc(L[ar.from], L[ar.to]) }));
  }
  function arc(a, b) {
    let bx = b.x, by = b.y; if (Math.abs(a.x - b.x) > MAP.W * 0.6) bx += a.x < b.x ? -MAP.W : MAP.W;      // round the edge
    const mx = (a.x + bx) / 2, my = (a.y + by) / 2 - Math.min(60, Math.hypot(bx - a.x, by - a.y) * 0.22);
    return `M${a.x} ${a.y}Q${mx} ${my} ${bx} ${by}`;
  }

  function clickLand(id) {
    if (!myTurn() || held) return;
    const { can, tg } = choices(), ph = S.phase;
    if (ph === 'claim') { if (can.has(id)) post({ t: 'claim', land: id }); return; }
    if (ph === 'setup' || ph === 'reinforce') {
      if (ph === 'reinforce' && S.hand.length >= 5) { openCards(); return; }
      if (can.has(id)) post({ t: 'place', land: id, n: perClick }); return;
    }
    if (ph === 'attack') {
      if (tg.has(id)) { battleOpen = { from: sel, to: id }; showBattle(); return; }
      if (can.has(id)) { sel = sel === id ? null : id; battleOpen = null; hideBattle(); paintGlow(); banner(); return; }
      return;
    }
    if (ph === 'fortify') {
      if (tg.has(id)) {
        const from = sel, max = S.lands[from].n - 1;
        askAmount(`March from ${L[from].name} to ${L[id].name}`, 1, max, max, n => { post({ t: 'fortify', from, to: id, n }); sel = null; }, true);
        return;
      }
      if (can.has(id)) { sel = sel === id ? null : id; paintGlow(); banner(); }
    }
  }

  // ------------------------------------------------------------ drawing the whole picture
  function show(id, on) { $(id).classList.toggle('hidden', !on); }
  let introDone = false, introSeen = false;
  function render() {
    if (!S) return;
    Faces.sync();
    const inGame = S.stage !== 'lobby';
    if (inGame) introSeen = introDone = true;            // the box is only opened once, before the first game
    if (!inGame && !introSeen && !qs.get('skip')) { introSeen = true; show('#intro', true); show('#game', false); show('#lobby', false); return; }
    if (!inGame && !introDone && !qs.get('skip') && introSeen && !$('#intro').classList.contains('hidden')) return;
    show('#intro', false); show('#lobby', !inGame); show('#game', inGame);
    if (!inGame) { show('#rejoin', false); firstBoard = true; lookAtBoard = false; show('#over', false); hideBattle(); show('#amount', false); return lobby(); }
    plaques(); board(); banner(); log(); cardsButton(); battleSync(); over();
    show('#rejoin', !SHOW && S.me < 0 && S.stage === 'game' && S.players.some(p => !p.bot && !p.on)); show('#quitBtn', S.me >= 0 && S.players[S.me].host);
    if (!$('#cards').classList.contains('hidden')) drawHand();
    firstBoard = false;
  }

  // lobby
  const SETUPS = [['place', 'Deal the lands', 'Lands are dealt at random. You place your armies, three at a time.'], ['claim', 'Choose the lands', 'Claim lands one by one in turn, then place your armies. The full ceremony.'], ['quick', 'Quick start', 'Everything is set out at random. Play begins at once.']];
  const GOALS = [['world', 'Conquer the world', 'Play until one commander remains.'], ['short', 'The Short War', 'First to hold thirty of the fifty lands wins.']];
  function lobby() {
    const me = S.players[S.me], host = me && me.host;
    $('#seats').innerHTML = S.players.map((p, i) => `<li><span class="seal ${cls(p.color)}"></span><span class="nm">${esc(p.name)}</span><span class="tag">${p.host ? 'host' : p.bot ? 'computer' : p.on ? '' : 'away'}</span>${host && !p.host ? `<button class="x" data-kick="${i}" title="Remove">×</button>` : ''}</li>`).join('') +
      (S.players.length < 2 ? '<li class="empty">Waiting for more commanders…</li>' : '');
    show('#joinBox', !me); show('#colorBox', !!me);
    if (me) $('#swatches').innerHTML = COLORS.map(c => { const taken = S.players.some(p => p !== me && p.color === c); return `<button class="${cls(c)}${me.color === c ? ' on' : ''}${taken ? ' taken' : ''}" data-c="${c}" ${taken ? 'disabled' : ''} title="${c}"></button>`; }).join('');
    const opt = (list, cur, key) => list.map(([v, b, s]) => `<button class="opt${cur === v ? ' on' : ''}" data-${key}="${v}"><i></i><div><b>${b}</b><span>${s}</span></div></button>`).join('');
    $('#optSetup').innerHTML = opt(SETUPS, S.opts.setup, 'setup'); $('#optGoal').innerHTML = opt(GOALS, S.opts.goal, 'goal');
    $('#optSetup').classList.toggle('locked', !host); $('#optGoal').classList.toggle('locked', !host);
    show('#addBot', host && S.players.length < 6); show('#startBtn', host);
    $('#startBtn').disabled = S.players.length < 2;
    $('#waitMsg').textContent = host ? (S.players.length < 2 ? 'Two or more commanders are needed.' : '') : !me ? 'Sign your name to take a seat.' : S.players.some(p => p.host) ? 'The host will begin the campaign when everyone is seated.' : 'Waiting for the host to sit down. The host is the person at the Mac that started the game.';
    const j = S.join;
    $('#joinSlip').innerHTML = `<b>In this house</b>Open Safari and go to<code>http://${j.ips[0] || j.host}:${j.port}</code>` + (j.far ? `<b style="margin-top:9px">From far away</b><code>${j.far}</code><i>Faces work through this link.</i>` : `<i>For family far away, start the game with "Start for far-away players".</i>`);
    show('#giftBtn', !!j.far && !!me);
  }

  const ICON = { land: '<svg viewBox="0 0 24 24"><path d="M5 21V4M5 5h12l-2.500 4L17 13H5"/></svg>', army: '<svg viewBox="0 0 24 24"><circle cx="12" cy="7" r="3.500"/><path d="M5 21c0-5 3-8 7-8s7 3 7 8"/></svg>', card: '<svg viewBox="0 0 24 24"><rect x="6" y="3" width="12" height="18" rx="2"/></svg>', plus: '<svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>' };
  function plaques() {
    const meHost = S.players[S.me] && S.players[S.me].host;
    $('#plaques').innerHTML = S.players.map((p, i) => `<div class="plaque ${cls(p.color)}${i === S.turn && S.stage === 'game' ? ' turn' : ''}${i === S.me ? ' me' : ''}${p.out ? ' out' : ''}${!p.on ? ' off' : ''}${meHost && !p.host && !p.out ? ' host-can' : ''}" data-i="${i}" title="${meHost && !p.host ? 'Click to let the computer play for ' + esc(p.name) + ', or to hand command back' : ''}">
      <span class="seal ${cls(p.color)}"></span><div><div class="p-name">${esc(p.name)}</div>
      <div class="p-stats"><span title="Lands held">${ICON.land}${p.lands}</span><span title="Armies on the board">${ICON.army}${p.armies}</span><span title="Cards in hand">${ICON.card}${p.cards}</span>${S.phase === 'setup' || S.phase === 'claim' ? `<span title="Armies still to place">${ICON.plus}${p.spare}</span>` : `<span title="New armies each turn">${ICON.plus}${p.income}</span>`}</div>
      ${p.bot ? '<div class="p-tag">computer</div>' : !p.on ? '<div class="p-tag">away</div>' : ''}</div></div>`).join('');
  }
  function fit() {                   // the board is as big as the space allows, whichever way the window is shaped
    const st = $('#stage'); if (!st.clientWidth) return;
    const tall = SHOW && innerWidth < 700 && innerHeight > innerWidth;      // a phone held upright: a tall board you swipe along
    document.body.classList.toggle('tall', tall);
    const w = tall ? (st.clientHeight - 30) * MAP.W / MAP.H : Math.max(200, Math.min(st.clientWidth - 36, (st.clientHeight - 10) * MAP.W / MAP.H));
    if (tall && !st.dataset.set) { st.dataset.set = 1; setTimeout(() => { st.scrollLeft = w * 0.42 - st.clientWidth / 2; }, 60); }
    const b = $('#board'); b.style.setProperty('--bw', Math.floor(w) + 'px'); b.style.setProperty('--bh', Math.floor(w * MAP.H / MAP.W) + 'px');
  }
  addEventListener('resize', () => { fit(); if (SHOW && S && S.stage === 'game') banner(); });
  function board() {
    fit();
    map.classList.toggle('tint', tint); $('#board').classList.toggle('tint', tint); $('#tintBtn').classList.toggle('on', tint);
    for (const t of LANDS) {
      const s = S.lands[t.id]; if (!s) continue; const col = s.o >= 0 ? S.players[s.o].color : null;
      N[t.id].land.setAttribute('class', 'land' + (col ? ' owned ' + cls(col) : ''));
      drawPiece(t.id, s.o, s.n, col);
    }
    if (sel && !choices().can.has(sel)) sel = null;
    paintGlow();
  }
  function log() { $('#chronicle').innerHTML = S.log.slice(-4).map(l => `<div>${esc(l.text)}</div>`).join(''); }

  function banner() {
    if (SHOW) {
      $('#steps').innerHTML = '<span class="on">Atlas of Empires</span>'; $('#bTitle').textContent = 'Have a look round';
      $('#bText').textContent = innerWidth < innerHeight && innerWidth < 700 ? 'This is our table. Swipe sideways to see the whole world.' : 'This is our table. We play together, each from home, on the day we choose.';
      show('#primary', false); show('#perClick', false); show('#facesBtn', false); $('#rulesBtn').classList.add('alert'); return;
    }
    const p = S.players[S.turn], me = myTurn(), ph = S.phase, name = p ? esc(p.name) : '';
    let title = '', text = '', btn = null, steps = ['Reinforce', 'Attack', 'March'], on = -1, pc = false;
    if (S.stage === 'over') { title = esc(S.players[S.winner].name) + ' rules the world'; text = 'The campaign is over.'; }
    else if (ph === 'claim') { steps = ['Choose the lands', 'Place armies', 'Begin']; on = 0; title = me ? 'Choose a land' : name + ' is choosing'; text = me ? 'Click any land that has no army on it.' : 'Lands are claimed one at a time, in turn.'; }
    else if (ph === 'setup') { steps = ['Lands', 'Place armies', 'Begin']; on = 1; title = me ? `Place ${S.setupLeft || Math.min(3, p.spare)} ${S.setupLeft === 1 ? 'army' : 'armies'}` : name + ' is placing armies'; text = me ? `Click your own lands. You have ${p.spare} left to place in all.` : `${p.spare} still to place.`; pc = me; }
    else if (ph === 'reinforce') {
      on = 0;
      if (me && S.hand.length >= 5) { title = 'Trade a set of cards'; text = 'You hold five or more cards, so a set must be traded first.'; btn = ['Open your cards', openCards]; }
      else if (me) { title = `Place ${S.pending} ${S.pending === 1 ? 'army' : 'armies'}`; text = S.mid ? 'Place the armies from your cards, then fight on.' : `Click your own lands to place them.${S.inc && S.inc.regs.length ? ' Includes the bonus for ' + S.inc.regs.map(r => REG[r].name).join(' and ') + '.' : ''}`; pc = true; }
      else { title = name + ' is reinforcing'; text = `${S.pending} ${S.pending === 1 ? 'army' : 'armies'} to place.`; }
    } else if (ph === 'attack') {
      on = 1;
      if (me) {
        if (S.movein) { title = 'The land is yours'; text = 'Choose how many more armies to send in.'; }
        else if (sel) { title = 'Attack from ' + L[sel].name; text = 'Click a glowing enemy land to attack it, or choose another of your lands.'; btn = ['Done attacking', () => { sel = null; hideBattle(); post({ t: 'endattack' }); }]; }
        else { title = 'Attack'; text = 'Click one of your lands, then the enemy land beside it. Or finish attacking.'; btn = ['Done attacking', () => { hideBattle(); post({ t: 'endattack' }); }]; }
      } else { title = name + ' is on the attack'; text = 'Watch your borders.'; }
    } else if (ph === 'fortify') {
      on = 2;
      if (me) { title = sel ? 'March from ' + L[sel].name : 'One march'; text = sel ? 'Click the land to march to.' : 'Move armies between two of your joined lands, or end your turn.'; btn = ['End turn', () => { sel = null; post({ t: 'endturn' }); }]; }
      else { title = name + ' is on the march'; text = ''; }
    }
    $('#steps').innerHTML = steps.map((s, i) => `<span class="${i === on ? 'on' : ''}">${s}</span>`).join('<i></i>');
    $('#bTitle').innerHTML = title; $('#bText').innerHTML = text + (me || S.stage === 'over' ? '' : '');
    const b = $('#primary'); show('#primary', !!btn); if (btn) { b.textContent = btn[0]; b.onclick = btn[1]; }
    show('#perClick', pc); document.querySelectorAll('#perClick button').forEach(x => x.classList.toggle('on', +x.dataset.n === perClick));
    document.title = me ? '● Your turn — Atlas of Empires' : 'Atlas of Empires';
    // moving in after a conquest
    if (me && S.movein && $('#amount').classList.contains('hidden') && !held && !moveT) {
      moveT = setTimeout(() => {        // let the winning dice be seen first
        moveT = null; if (!S.movein || !myTurn()) return;
        const mv = S.movein; clearTimeout(watchT); hideBattle();
        askAmount(`${L[mv.to].name} is taken. Send more armies in?`, 0, mv.max, mv.max, n => post({ t: 'movein', n }), false);
      }, 1300);
    }
    if ((!me || !S.movein) && amountCb && amountCb.forMove) { show('#amount', false); amountCb = null; }
  }

  // ------------------------------------------------------------ battle
  let battleShown = null, watchT = null, moveT = null;
  const pips = n => { const on = { 1: [4], 2: [0, 8], 3: [0, 4, 8], 4: [0, 2, 6, 8], 5: [0, 2, 4, 6, 8], 6: [0, 2, 3, 5, 6, 8] }[n] || []; return Array.from({ length: 9 }, (_, i) => `<i class="${on.includes(i) ? 'on' : ''}"></i>`).join(''); };
  function fillBattle(from, to, attI, defI) {
    const a = S.players[attI], d = S.players[defI], A = S.lands[from], D = S.lands[to];
    $('#bAttName').textContent = a.name; $('#bAttLand').textContent = L[from].name; $('#bAttN').innerHTML = A.n + '<small>' + (A.n === 1 ? 'army' : 'armies') + '</small>'; $('#bAttN').className = 'b-n';
    $('#bDefName').textContent = d ? d.name : ''; $('#bDefLand').textContent = L[to].name; $('#bDefN').innerHTML = D.n + '<small>' + (D.n === 1 ? 'army' : 'armies') + '</small>';
    $('#battle').dataset.a = cls(a.color); $('#battle').dataset.d = d ? cls(d.color) : '';
  }
  function showBattle() {
    if (!battleOpen) return;
    const { from, to } = battleOpen, A = S.lands[from], D = S.lands[to];
    if (!mine(from) || mine(to) || A.n < 2) { battleOpen = null; return hideBattle(); }
    battleShown = { from, to }; clearTimeout(watchT);
    fillBattle(from, to, S.me, D.o);
    const max = Math.min(3, A.n - 1);
    if (!$('#diceA').dataset.keep) { $('#diceA').innerHTML = dice(max, cls(S.players[S.me].color), null); $('#diceD').innerHTML = dice(Math.min(2, D.n), $('#battle').dataset.d, null); $('#bResult').textContent = 'Choose how many dice to roll.'; }
    const B = $('#bBtns'); B.innerHTML = '';
    for (let n = max; n >= 1; n--) { const b = el('button', 'brass', `Roll ${n} ${n === 1 ? 'die' : 'dice'}`); b.onclick = () => post({ t: 'attack', from, to, dice: n }); B.appendChild(b); }
    const bl = el('button', 'brass', 'Fight to the end'); bl.onclick = () => post({ t: 'attack', from, to, blitz: true }); B.appendChild(bl);
    const r = el('button', 'ghost', 'Fall back'); r.onclick = () => { battleOpen = null; hideBattle(); }; B.appendChild(r);
    show('#battle', true); paintGlow();
  }
  function hideBattle() { show('#battle', false); battleShown = null; delete $('#diceA').dataset.keep; if (S && S.stage !== 'lobby') paintGlow(); }
  const dice = (n, c, vals) => Array.from({ length: n }, (_, i) => `<div class="die ${c}">${pips(vals ? vals[i] : 1 + Math.floor(Math.random() * 6))}</div>`).join('');
  let rollT = null;
  function rollDice(b) {             // dice tumble while the new picture of the game is held back
    const r = b.rolls[0], a = S.players[b.att], d = S.players[b.def];
    battleShown = { from: b.from, to: b.to }; clearTimeout(watchT);
    $('#bAttName').textContent = a.name; $('#bAttLand').textContent = L[b.from].name; $('#bDefName').textContent = d.name; $('#bDefLand').textContent = L[b.to].name;
    $('#battle').dataset.a = cls(a.color); $('#battle').dataset.d = cls(d.color);
    if ($('#battle').classList.contains('hidden')) { $('#bAttN').innerHTML = S.lands[b.from].n + '<small>armies</small>'; $('#bDefN').innerHTML = S.lands[b.to].n + '<small>armies</small>'; }
    $('#diceA').innerHTML = dice(r.a.length, cls(a.color)); $('#diceD').innerHTML = dice(r.d.length, cls(d.color));
    document.querySelectorAll('#battle .die').forEach(x => x.classList.add('roll'));
    $('#bResult').textContent = b.n > 1 ? `Fighting to the end…` : 'The dice are cast…';
    $('#bBtns').innerHTML = b.att === S.me ? '' : `<span class="watch">${esc(a.name)} attacks ${esc(d.name)}</span>`;
    show('#battle', true); paintGlow();
    clearInterval(rollT); rollT = setInterval(() => document.querySelectorAll('#battle .die.roll').forEach(x => x.innerHTML = pips(1 + Math.floor(Math.random() * 6))), 70);
  }
  function settleDice(b) {
    clearInterval(rollT);
    const r = b.rolls[0], a = S.players[b.att], d = S.players[b.def];
    $('#diceA').innerHTML = dice(r.a.length, cls(a.color), r.a); $('#diceD').innerHTML = dice(r.d.length, cls(d.color), r.d); $('#diceA').dataset.keep = 1;
    const da = [...$('#diceA').children], dd = [...$('#diceD').children];
    [...da, ...dd].forEach(x => x.classList.add('land-in'));
    for (let k = 0; k < Math.min(da.length, dd.length); k++) { const aw = r.a[k] > r.d[k]; da[k].classList.add(aw ? 'win' : 'lose'); dd[k].classList.add(aw ? 'lose' : 'win'); }
    const parts = []; if (b.al) parts.push(`${esc(a.name)} loses ${b.al}`); if (b.dl) parts.push(`${esc(d.name)} loses ${b.dl}`);
    $('#bResult').innerHTML = (b.n > 1 ? `After ${b.n} rolls: ` : '') + parts.join(' · ') + (b.won ? ` — <b>${esc(L[b.to].name)} falls!</b>` : '');
    if (b.al) floater(b.from, '−' + b.al); if (b.dl) floater(b.to, '−' + b.dl); if (b.won) setTimeout(() => floater(b.to, 'Conquered', true), 350);
  }
  function battleSync() {            // after each new picture: keep the panel right for attacker and watchers
    const b = S.battle;
    if (battleShown) {
      const { from, to } = battleShown;
      const A = S.lands[from], D = S.lands[to];
      $('#bAttN').innerHTML = A.n + '<small>' + (A.n === 1 ? 'army' : 'armies') + '</small>'; $('#bDefN').innerHTML = D.n + '<small>' + (D.n === 1 ? 'army' : 'armies') + '</small>';
    }
    if (myTurn() && S.phase === 'attack' && battleOpen && !S.movein && mine(battleOpen.from) && !mine(battleOpen.to) && S.lands[battleOpen.from].n >= 2) { showBattle(); return; }
    if (battleOpen) { battleOpen = null; }
    if (battleShown) { $('#bBtns').innerHTML = $('#bBtns').querySelector('.watch') ? $('#bBtns').innerHTML : ''; clearTimeout(watchT); watchT = setTimeout(hideBattle, myTurn() ? 1500 : 2600); }
  }
  function floater(id, text, good) {
    const t = L[id], f = el('div', 'floater' + (good ? ' good' : ''), text);
    f.style.left = (t.x / MAP.W * 100) + '%'; f.style.top = (t.y / MAP.H * 100) + '%';
    $('#floaters').appendChild(f); setTimeout(() => f.remove(), 1600);
  }

  // ------------------------------------------------------------ choosing a number
  function askAmount(title, min, max, start, cb, canCancel) {
    amountCb = { cb, forMove: !canCancel };
    $('#amTitle').textContent = title; const r = $('#amRange'); r.min = min; r.max = max; r.value = start; $('#amNum').textContent = start;
    r.style.visibility = max > min ? 'visible' : 'hidden';
    show('#amCancel', canCancel); show('#amount', true);
  }
  $('#amRange').oninput = e => $('#amNum').textContent = e.target.value;
  const nudge = d => { const r = $('#amRange'); r.value = Math.max(+r.min, Math.min(+r.max, +r.value + d)); $('#amNum').textContent = r.value; };
  $('#amMinus').onclick = () => nudge(-1); $('#amPlus').onclick = () => nudge(1);
  $('#amOk').onclick = () => { const c = amountCb; amountCb = null; show('#amount', false); if (c) c.cb(+$('#amRange').value); };
  $('#amCancel').onclick = () => { amountCb = null; show('#amount', false); };

  // ------------------------------------------------------------ cards
  const SYM = { compass: 'Compass', anchor: 'Anchor', crown: 'Crown' };
  function validSet(cs) { if (cs.length !== 3) return false; const s = cs.map(c => c.sym); if (s.includes('wild')) return true; const u = new Set(s).size; return u === 1 || u === 3; }
  function hasSet(h) { for (let a = 0; a < h.length; a++) for (let b = a + 1; b < h.length; b++) for (let c = b + 1; c < h.length; c++) if (validSet([h[a], h[b], h[c]])) return [a, b, c]; return null; }
  function cardsButton() {
    const n = S.hand.length, c = $('#cardCount'); c.textContent = n; c.classList.toggle('zero', !n);
    $('#cardsBtn').classList.toggle('alert', myTurn() && S.phase === 'reinforce' && !!hasSet(S.hand));
  }
  function shape(t) {
    const tmp = sv('path', { d: t.d }); gFx.appendChild(tmp); const b = tmp.getBBox(); tmp.remove();
    const pad = Math.max(b.width, b.height) * 0.06;
    return `<svg class="shape" viewBox="${b.x - pad} ${b.y - pad} ${b.width + 2 * pad} ${b.height + 2 * pad}" style="--tint:${REG[t.region].tint}"><path d="${t.d}" fill-rule="evenodd"/></svg>`;
  }
  function drawHand() {
    const h = S.hand; chosen = new Set([...chosen].filter(i => i < h.length));
    const canTrade = myTurn() && S.phase === 'reinforce';
    $('#hand').innerHTML = h.length ? h.map((c, i) => {
      if (c.sym === 'wild') return `<div class="card wild${chosen.has(i) ? ' on' : ''}" data-i="${i}" style="animation-delay:${i * 0.06}s"><div class="c-reg">Completes any set</div><div class="c-name">Wild Card</div><div class="embs"><img src="img/compass.png"><img src="img/anchor.png"><img src="img/crown.png"></div><div class="c-sym">Any emblem</div></div>`;
      const t = L[c.land];
      return `<div class="card${chosen.has(i) ? ' on' : ''}${mine(c.land) ? ' mine' : ''}" data-i="${i}" style="animation-delay:${i * 0.06}s"><div class="c-reg">${REG[t.region].name}</div><div class="c-name">${t.name}</div>${shape(t)}<img class="emb" src="img/${c.sym}.png"><div class="c-sym">${SYM[c.sym]}</div></div>`;
    }).join('') : '<div class="nocards">You hold no cards yet. Conquer a land on your turn to earn one.</div>';
    const ok = validSet([...chosen].map(i => h[i]));
    $('#cardsHelp').textContent = !h.length ? '' : canTrade ? `A set is three alike, or one of each. The next set is worth ${S.nextSet} armies.` : `Sets can be traded at the start of your own turn. The next set is worth ${S.nextSet} armies.`;
    const b = $('#tradeBtn'); show('#tradeBtn', canTrade && h.length >= 3); b.disabled = !ok; b.textContent = ok ? `Trade for ${S.nextSet} armies` : 'Choose three cards';
  }
  function openCards() { const s = myTurn() && S.phase === 'reinforce' ? hasSet(S.hand) : null; chosen = new Set(s || []); show('#cards', true); drawHand(); }
  $('#hand').onclick = e => { const c = e.target.closest('.card'); if (!c) return; const i = +c.dataset.i; if (chosen.has(i)) chosen.delete(i); else if (chosen.size < 3) chosen.add(i); document.querySelectorAll('#hand .card').forEach(x => { x.style.animation = 'none'; }); drawHandKeep(); };
  function drawHandKeep() { document.querySelectorAll('#hand .card').forEach(x => x.classList.toggle('on', chosen.has(+x.dataset.i))); const ok = validSet([...chosen].map(i => S.hand[i])); const b = $('#tradeBtn'); b.disabled = !ok; b.textContent = ok ? `Trade for ${S.nextSet} armies` : 'Choose three cards'; }
  $('#tradeBtn').onclick = () => { post({ t: 'trade', cards: [...chosen] }).then(o => { chosen = new Set(); if (o && !o.err && !(S.hand.length - 3 >= 5)) show('#cards', false); }); };
  $('#cardsClose').onclick = () => show('#cards', false);
  $('#cardsBtn').onclick = openCards;

  // ------------------------------------------------------------ the rule book
  function drawBook(flip) {
    const pl = $('#pageL'), pr = $('#pageR');
    pl.innerHTML = RULES[bookAt] || ''; pr.innerHTML = RULES[bookAt + 1] || '';
    if (flip) { for (const p of [pl, pr]) { p.classList.remove('flip'); void p.offsetWidth; p.classList.add('flip'); } }
    $('#bkPrev').disabled = bookAt === 0; $('#bkNext').disabled = bookAt + 2 >= RULES.length;
  }
  const openBook = () => { show('#book', true); drawBook(); };
  $('#bkPrev').onclick = () => { bookAt = Math.max(0, bookAt - 2); drawBook(true); };
  $('#bkNext').onclick = () => { if (bookAt + 2 < RULES.length) bookAt += 2; drawBook(true); };
  $('#bkClose').onclick = () => show('#book', false);
  $('#rulesBtn').onclick = openBook; $('#bookBtn').onclick = openBook;
  for (const o of document.querySelectorAll('.overlay')) o.addEventListener('click', e => { if (e.target === o && o.id !== 'over') show('#' + o.id, false); });
  addEventListener('keydown', e => {
    if (e.key === 'Escape') { for (const id of ['#book', '#cards']) show(id, false); }
    if (!$('#book').classList.contains('hidden')) { if (e.key === 'ArrowRight') $('#bkNext').click(); if (e.key === 'ArrowLeft') $('#bkPrev').click(); }
  });

  // ------------------------------------------------------------ the end
  function over() {
    const on = S.stage === 'over' && !lookAtBoard; show('#over', on); if (!on) return;
    const w = S.players[S.winner];
    $('#overName').textContent = w.name; $('#overLine').textContent = S.opts.goal === 'short' && S.players.filter(p => !p.out).length > 1 ? `holds ${w.lands} lands and wins the Short War, in ${S.round} rounds.` : `rules the world, after ${S.round} rounds.`;
    $('#overTable').innerHTML = [...S.players].sort((a, b) => b.lands - a.lands).map(p => `<tr><td><span class="seal ${cls(p.color)}"></span>${esc(p.name)}</td><td>${p.lands ? p.lands + ' lands, ' + p.armies + ' armies' : 'defeated'}</td></tr>`).join('');
    show('#againBtn', S.players[S.me] && S.players[S.me].host);
  }
  $('#againBtn').onclick = () => post({ t: 'again' });
  $('#overLook').onclick = () => { lookAtBoard = true; show('#over', false); };

  // ------------------------------------------------------------ buttons
  $('#tintBtn').onclick = () => { tint = !tint; board(); };
  $('#perClick').onclick = e => { const b = e.target.closest('button'); if (b) { perClick = +b.dataset.n; banner(); } };
  $('#plaques').onclick = e => { const p = e.target.closest('.plaque.host-can'); if (p) post({ t: 'auto', i: +p.dataset.i }); };
  $('#seats').onclick = e => { const b = e.target.closest('[data-kick]'); if (b) post({ t: 'kick', i: +b.dataset.kick }); };
  $('#swatches').onclick = e => { const b = e.target.closest('button'); if (b && !b.disabled) post({ t: 'color', c: b.dataset.c }); };
  $('#optSetup').onclick = e => { const b = e.target.closest('.opt'); if (b) post({ t: 'opts', setup: b.dataset.setup }); };
  $('#optGoal').onclick = e => { const b = e.target.closest('.opt'); if (b) post({ t: 'opts', goal: b.dataset.goal }); };
  $('#addBot').onclick = () => post({ t: 'addbot' });
  $('#startBtn').onclick = () => post({ t: 'start' });
  function join() {
    const name = $('#nameIn').value.trim(); if (!name) { $('#nameIn').focus(); return toast('Sign your name first.'); }
    store.set('aoe_name', name);
    fetch('/act', { method: 'POST', body: JSON.stringify({ t: 'join', name, pid }) }).then(r => r.json()).then(o => { if (o.err) return toast(o.err); pid = o.pid; store.set('aoe_pid' + SEAT, pid); listen(); });
  }
  function rejoin() {
    const name = $('#rejoinIn').value.trim(); if (!name) return $('#rejoinIn').focus();
    fetch('/act', { method: 'POST', body: JSON.stringify({ t: 'join', name, pid }) }).then(r => r.json()).then(o => { if (o.err) return toast(o.err); pid = o.pid; store.set('aoe_pid' + SEAT, pid); listen(); });
  }
  $('#rejoinBtn').onclick = rejoin; $('#rejoinIn').addEventListener('keydown', e => { if (e.key === 'Enter') rejoin(); });
  let quitArmed = 0;
  $('#quitBtn').onclick = () => { if (Date.now() - quitArmed < 4000) { quitArmed = 0; post({ t: 'again' }); } else { quitArmed = Date.now(); toast('Click once more to abandon this game for everyone.'); } };
  $('#seeBoard').onclick = () => show('#boardPeek', true); $('#peekClose').onclick = () => show('#boardPeek', false);
  $('#facesBtn').onclick = Faces.toggle; $('#facesLobby').onclick = Faces.toggle;
  $('#gMic').onclick = Faces.mic; $('#gCam').onclick = Faces.cam; $('#gSound').onclick = Faces.sound; $('#gOff').onclick = Faces.stop;
  addEventListener('resize', () => Faces.sync());

  // the gift maker: a link that arrives wrapped, to send by WhatsApp
  const giftLink = () => { const to = $('#gmTo').value.trim(), from = $('#gmFrom').value.trim(); return (S.join.far || location.origin) + '/gift?to=' + encodeURIComponent(to) + (from ? '&from=' + encodeURIComponent(from) : ''); };
  const drawGift = () => { $('#gmLink').textContent = giftLink(); };
  $('#giftBtn').onclick = () => { if (!$('#gmFrom').value && S.players[S.me]) $('#gmFrom').value = S.players[S.me].name; show('#giftMaker', true); drawGift(); $('#gmTo').focus(); };
  $('#gmTo').oninput = drawGift; $('#gmFrom').oninput = drawGift;
  $('#gmClose').onclick = () => show('#giftMaker', false);
  $('#gmCopy').onclick = () => { const t = giftLink(); (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(() => toast('The gift link is copied. Paste it into WhatsApp.'), () => toast('Select the link and copy it by hand.')); };
  $('#gmWa').onclick = () => { const to = $('#gmTo').value.trim(); window.open('https://wa.me/?text=' + encodeURIComponent((to ? to + ', a' : 'A') + ' gift for you. Untie the ribbon: ' + giftLink()), '_blank'); };
  $('#joinBtn').onclick = join; $('#nameIn').addEventListener('keydown', e => { if (e.key === 'Enter') join(); });
  $('#nameIn').value = SEAT ? '' : store.get('aoe_name');

  // arriving as a gift: the box comes wrapped, with a tag
  const GIFT = SHOW || location.pathname.replace(/\/$/, '') === '/gift';
  if (GIFT) {
    const to = (qs.get('to') || '').slice(0, 20), from = (qs.get('from') || '').slice(0, 20);
    $('#intro').classList.add('gift'); $('#tagTo').textContent = to || 'you'; $('#tagFrom').textContent = from ? 'from ' + from : '';
    if (to && !store.get('aoe_name')) $('#nameIn').value = to;
    $('#untie').onclick = () => { $('#intro').classList.add('shake'); setTimeout(() => $('#intro').classList.add('unwrapped'), 650); };
  }
  // the box
  $('#openBox').onclick = () => {
    $('#intro').classList.add('open');
    setTimeout(() => $('#intro').classList.add('away'), 2300);
    setTimeout(() => { introDone = true; if (SHOW) { S = showState('game'); render(); setTimeout(() => toast('Open the book, bottom right, to read the rules.'), 2600); return; } render(); if (!S.players[S.me]) $('#nameIn').focus(); }, 3200);
  };
  // if a game is already running and this Mac has no seat, offer the name box so a player can take their seat again
  listen();
})();
