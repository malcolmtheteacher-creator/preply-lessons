/* Hall of Thought: a walkable 3D gallery. Everything is real geometry (Three.js r128). */
(function () {
  const T = THREE;
  const W = 28, L = 30, H = 11, DOOR = 3.6;         // chamber width, length, height, door half-width
  const zc = i => -(i * L + L / 2);                  // chamber centre z
  const animated = [];

  // ---------- renderer / scene ----------
  const renderer = new T.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setSize(innerWidth, innerHeight);
  document.body.appendChild(renderer.domElement);
  const scene = new T.Scene();
  scene.background = new T.Color(0x0b0a10);
  scene.fog = new T.FogExp2(0x0b0a10, 0.018);
  const camera = new T.PerspectiveCamera(70, innerWidth / innerHeight, 0.1, 300);
  scene.add(new T.HemisphereLight(0xfff2dd, 0x2a2438, 0.75));

  // ---------- materials & textures ----------
  const marble = new T.MeshStandardMaterial({ color: 0xf1ede4, roughness: 0.55, metalness: 0.02, side: T.DoubleSide });
  const stoneDark = new T.MeshStandardMaterial({ color: 0x4d4859, roughness: 0.8 });
  const gold = new T.MeshStandardMaterial({ color: 0xd4af37, roughness: 0.3, metalness: 0.8 });
  const glow = (c, i = 1) => new T.MeshStandardMaterial({ color: c, emissive: c, emissiveIntensity: i, roughness: 0.4 });
  const glass = (c, o = 0.3) => new T.MeshStandardMaterial({ color: c, transparent: true, opacity: o, roughness: 0.1, metalness: 0.1, side: T.DoubleSide, depthWrite: false });
  const wire = c => new T.MeshBasicMaterial({ color: c, wireframe: true });
  const mesh = (g, m, x = 0, y = 0, z = 0) => { const o = new T.Mesh(g, m); o.position.set(x, y, z); return o; };

  function canvasTex(w, h, draw) {
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    const g = c.getContext('2d'); draw(g, w, h);
    const t = new T.CanvasTexture(c); t.anisotropy = 4; return t;
  }
  function wrapText(g, text, x, y, maxW, lh, align) {
    const words = text.split(' '); let line = ''; const lines = [];
    for (const w of words) { const t = line ? line + ' ' + w : w; if (g.measureText(t).width > maxW && line) { lines.push(line); line = w; } else line = t; }
    lines.push(line);
    g.textAlign = align || 'center';
    lines.forEach((l, i) => g.fillText(l, x, y + i * lh));
    return lines.length;
  }
  const floorTex = canvasTex(256, 256, (g, w, h) => {
    g.fillStyle = '#fff'; g.fillRect(0, 0, w, h);
    g.fillStyle = '#d9d4c6'; g.fillRect(0, 0, w / 2, h / 2); g.fillRect(w / 2, h / 2, w / 2, h / 2);
    for (let i = 0; i < 1800; i++) { g.fillStyle = `rgba(120,110,100,${Math.random() * 0.05})`; g.fillRect(Math.random() * w, Math.random() * h, 2, 2); }
    g.strokeStyle = 'rgba(90,80,70,.35)'; g.lineWidth = 2; g.strokeRect(0, 0, w, h); g.beginPath(); g.moveTo(w / 2, 0); g.lineTo(w / 2, h); g.moveTo(0, h / 2); g.lineTo(w, h / 2); g.stroke();
  });
  floorTex.wrapS = floorTex.wrapT = T.RepeatWrapping; floorTex.repeat.set(W / 3.5, L / 3.5);
  const starTex = canvasTex(512, 512, (g, w, h) => {
    g.fillStyle = '#070612'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 260; i++) { g.fillStyle = `rgba(255,255,255,${0.3 + Math.random() * 0.7})`; const s = Math.random() * 1.8 + 0.4; g.fillRect(Math.random() * w, Math.random() * h, s, s); }
  });
  starTex.wrapS = starTex.wrapT = T.RepeatWrapping; starTex.repeat.set(3, 3);

  function labelSprite(text, size = 1, color = '#fff', bg) {
    const tex = canvasTex(1024, 128, (g, w, h) => {
      g.font = '600 64px Georgia, serif'; g.textAlign = 'center'; g.textBaseline = 'middle';
      if (bg) { g.fillStyle = bg; g.fillRect(0, 0, w, h); }
      g.shadowColor = 'rgba(0,0,0,.8)'; g.shadowBlur = 10; g.fillStyle = color; g.fillText(text, w / 2, h / 2 + 3);
    });
    const s = new T.Sprite(new T.SpriteMaterial({ map: tex, transparent: true, depthWrite: false, fog: false }));
    s.scale.set(8 * size, size, 1); return s;
  }

  // ---------- books ----------
  const PAL = [0x7b2d26, 0x1f4e5f, 0x3b5d2c, 0x4a3a6b, 0x8a5a1e, 0x2d3e63, 0x6b2a4a, 0x2f2f2f];
  const coverCache = {};
  function coverMat(title, vertical) {
    const key = title + (vertical ? 'v' : 'h');
    if (coverCache[key]) return coverCache[key];
    let hsh = 0; for (const ch of title) hsh = (hsh * 31 + ch.charCodeAt(0)) >>> 0;
    const col = '#' + PAL[hsh % PAL.length].toString(16).padStart(6, '0');
    const tex = canvasTex(256, 340, (g, w, h) => {
      g.fillStyle = col; g.fillRect(0, 0, w, h);
      g.strokeStyle = '#d4af37'; g.lineWidth = 5; g.strokeRect(14, 14, w - 28, h - 28);
      g.strokeStyle = 'rgba(212,175,55,.5)'; g.lineWidth = 2; g.strokeRect(24, 24, w - 48, h - 48);
      g.fillStyle = '#f3e6bd'; g.font = '700 28px Georgia, serif'; g.textBaseline = 'middle';
      const clean = title.replace(/: A Very Short Introduction/, '');
      const n = wrapText(g, clean, w / 2, h / 2 - 20, w - 70, 34);
      if (/Very Short/.test(title)) { g.font = 'italic 17px Georgia'; g.fillStyle = '#d4af37'; g.fillText('A Very Short Introduction', w / 2, h / 2 + n * 34 - 6); }
      g.fillStyle = '#d4af37'; g.fillRect(w / 2 - 28, h - 70, 56, 3);
    });
    const front = new T.MeshStandardMaterial({ map: tex, roughness: 0.7 });
    const paper = new T.MeshStandardMaterial({ color: 0xece0c0, roughness: 0.9 });
    const spine = new T.MeshStandardMaterial({ color: new T.Color(col), roughness: 0.7 });
    return (coverCache[key] = { front, paper, spine });
  }
  const bookGeo = new T.BoxGeometry(0.9, 0.13, 1.2);
  function lyingBook(title) {
    const m = coverMat(title, false);
    // +x,-x,+y,-y,+z,-z
    return new T.Mesh(bookGeo, [m.paper, m.spine, m.front, m.spine, m.paper, m.paper]);
  }
  function bookTable(titles) {
    const g = new T.Group();
    g.add(mesh(new T.BoxGeometry(1.7, 0.6, 1.4), stoneDark, 0, 0.3, 0));
    g.add(mesh(new T.BoxGeometry(1.8, 0.07, 1.5), gold, 0, 0.63, 0));
    let y = 0.7;
    titles.slice(0, 4).forEach((t, i) => {
      const b = lyingBook(t); b.position.set((i % 2 ? 0.06 : -0.05), y + 0.065, (i % 2 ? -0.04 : 0.03)); b.rotation.y = (i - 1.5) * 0.12; g.add(b); y += 0.14;
    });
    return g;
  }

  // ---------- statue ----------
  const hairMat = new T.MeshStandardMaterial({ color: 0xa89f8c, roughness: 0.85 });
  function limb(a, b, r) {
    const d = b.clone().sub(a), len = d.length();
    const m = new T.Mesh(new T.CylinderGeometry(r, r * 0.85, len, 8), marble);
    m.position.copy(a).add(b).multiplyScalar(0.5);
    m.quaternion.setFromUnitVectors(new T.Vector3(0, 1, 0), d.normalize()); return m;
  }
  const POSES = {
    rest:  { R: [0.40, 1.0, 0.10],  L: [-0.40, 1.0, 0.10] },
    up:    { R: [0.40, 2.30, 0.15], L: [-0.30, 1.25, 0.32] },
    point: { R: [0.65, 1.45, 0.70], L: [-0.30, 1.20, 0.30] },
    think: { R: [0.07, 1.62, 0.22], L: [-0.12, 1.20, 0.26] },
    book:  { R: [0.14, 1.18, 0.38], L: [-0.14, 1.18, 0.38] },
    wide:  { R: [0.80, 1.90, 0.20], L: [-0.80, 1.90, 0.20] },
    scroll:{ R: [0.30, 1.20, 0.38], L: [-0.18, 1.22, 0.34] },
    lap:   { R: [0.20, 0.70, 0.42], L: [-0.20, 0.70, 0.42] },
  };
  function makeStatue(c) {
    const g = new T.Group(), seated = !!c.seated, Hs = seated ? 1.1 : 1.5;
    const prof = seated
      ? [[0, 0.3], [0.38, 0.3], [0.31, 0.6], [0.26, 0.85], [0.3, 1.0], [0.22, 1.1], [0.09, 1.18], [0.08, 1.26]]
      : [[0, 0], [0.45, 0], [0.44, 0.06], [0.33, 0.7], [0.27, 1.1], [0.3, 1.38], [0.22, 1.5], [0.09, 1.58], [0.08, 1.66]];
    g.add(new T.Mesh(new T.LatheGeometry(prof.map(p => new T.Vector2(p[0], p[1])), 28), marble));
    if (seated) { const lap = mesh(new T.SphereGeometry(1, 20, 12), marble, 0, 0.22, 0.05); lap.scale.set(0.75, 0.24, 0.55); g.add(lap); }
    const hy = Hs + 0.32, hm = hairMat;
    const head = new T.Group(); head.position.set(0, hy, 0); g.add(head);
    head.add(new T.Mesh(new T.SphereGeometry(0.17, 20, 16), marble));
    const nose = mesh(new T.ConeGeometry(0.03, 0.08, 8), marble, 0, -0.01, 0.17); nose.rotation.x = Math.PI / 2; head.add(nose);
    for (const sx of [-1, 1]) { const e = mesh(new T.SphereGeometry(0.028, 8, 6), stoneDark, sx * 0.065, 0.04, 0.155); e.scale.z = 0.5; head.add(e); }
    const shl = mesh(new T.SphereGeometry(1, 16, 10), marble, 0, Hs - 0.08, 0); shl.scale.set(0.42, 0.15, 0.24); g.add(shl);
    // hair
    if (c.hair === 'short' || c.hair === 'long') {
      const cap = mesh(new T.SphereGeometry(0.185, 18, 12, 0, 6.283, 0, 1.7), hm, 0, 0.01, -0.02); cap.rotation.x = -0.25; head.add(cap);
      if (c.hair === 'long') head.add(mesh(new T.CylinderGeometry(0.17, 0.12, 0.5, 12), hm, 0, -0.2, -0.1));
    }
    if (c.hair === 'wild') for (let i = 0; i < 28; i++) {
      const a = Math.random() * 6.283, e = Math.random() * 1.2 - 0.2, cone = new T.Mesh(new T.ConeGeometry(0.045, 0.25, 6), hm);
      cone.position.set(Math.cos(a) * Math.cos(e) * 0.19, Math.sin(e) * 0.19 + 0.04, Math.sin(a) * Math.cos(e) * 0.19 - 0.02);
      cone.lookAt(cone.position.clone().multiplyScalar(3)); cone.rotateX(Math.PI / 2); head.add(cone);
    }
    if (c.beard === 'long') { const b = mesh(new T.ConeGeometry(0.14, 0.55, 12), hm, 0, -0.34, 0.07); b.rotation.x = Math.PI + 0.1; head.add(b); }
    if (c.beard === 'short') { const b = mesh(new T.SphereGeometry(1, 12, 8), hm, 0, -0.13, 0.09); b.scale.set(0.14, 0.13, 0.1); head.add(b); }
    if (c.mous) { const s = c.mous === 'big' ? 2 : 1; for (const sx of [-1, 1]) { const m = mesh(new T.SphereGeometry(1, 10, 8), hm, sx * 0.05 * s, -0.07, 0.165); m.scale.set(0.055 * s, 0.025 * s, 0.035); m.rotation.z = -sx * 0.25; head.add(m); } }
    if (c.glasses) for (const sx of [-1, 1]) head.add(mesh(new T.TorusGeometry(0.05, 0.009, 6, 16), gold, sx * 0.075, 0.035, 0.168));
    const hats = {
      laurel: () => mesh(new T.TorusGeometry(0.175, 0.02, 6, 20), hm, 0, 0.09, 0).rotateX(Math.PI / 2),
      turban: () => { const t = new T.Group(); t.add(mesh(new T.TorusGeometry(0.16, 0.08, 10, 20), hm, 0, 0.1, 0).rotateX(Math.PI / 2)); const d = mesh(new T.SphereGeometry(1, 14, 10), hm, 0, 0.19, 0); d.scale.set(0.2, 0.13, 0.2); t.add(d); return t; },
      cap: () => mesh(new T.CylinderGeometry(0.14, 0.19, 0.22, 14), hm, 0, 0.19, 0),
      beret: () => { const b = mesh(new T.CylinderGeometry(0.24, 0.2, 0.06, 18), hm, 0.04, 0.17, 0); b.rotation.z = -0.15; return b; },
      topknot: () => mesh(new T.SphereGeometry(0.06, 10, 8), hm, 0, 0.2, -0.02),
      ushnisha: () => { const t = new T.Group(); for (let i = 0; i < 14; i++) { const a = i * 2.4, r = 0.12 * Math.sin(i * 0.4 + 0.5); t.add(mesh(new T.SphereGeometry(0.035, 6, 5), hm, Math.cos(a) * r, 0.13 + i * 0.008, Math.sin(a) * r)); } t.add(mesh(new T.SphereGeometry(0.075, 10, 8), hm, 0, 0.21, 0)); return t; },
      hood: () => { const h = mesh(new T.SphereGeometry(0.23, 16, 12, 0, 6.283, 0, 2.2), hm, 0, 0.0, -0.04); h.rotation.x = -0.35; return h; },
      skullcap: () => mesh(new T.SphereGeometry(0.18, 14, 10, 0, 6.283, 0, 1.0), hm, 0, 0.06, 0),
      wig: () => { const t = new T.Group(); t.add(mesh(new T.SphereGeometry(0.2, 16, 12, 0, 6.283, 0, 1.9), hm, 0, 0.02, -0.02)); for (const sx of [-1, 1]) for (let i = 0; i < 3; i++) t.add(mesh(new T.SphereGeometry(0.045, 8, 6), hm, sx * 0.19, -0.04 - i * 0.045, 0.0)); return t; },
      tophat: () => { const t = new T.Group(); t.add(mesh(new T.CylinderGeometry(0.22, 0.22, 0.02, 18), hm, 0, 0.14, 0)); t.add(mesh(new T.CylinderGeometry(0.13, 0.14, 0.26, 16), hm, 0, 0.27, 0)); return t; },
    };
    if (c.hat && hats[c.hat]) head.add(hats[c.hat]());
    // arms
    const pose = POSES[c.pose] || POSES.rest;
    for (const [side, key] of [[1, 'R'], [-1, 'L']]) {
      const sh = new T.Vector3(side * 0.3, Hs - 0.08, 0), hand = new T.Vector3(...pose[key]);
      if (seated) hand.y -= 0; const el = sh.clone().add(hand).multiplyScalar(0.5).add(new T.Vector3(side * 0.14, -0.14, 0.1));
      g.add(limb(sh, el, 0.075), limb(el, hand, 0.06), mesh(new T.SphereGeometry(0.07, 8, 6), marble, hand.x, hand.y, hand.z));
      if (key === 'L' && c.book) { const bk = mesh(new T.BoxGeometry(0.34, 0.44, 0.08), marble, hand.x + 0.06, hand.y + 0.02, hand.z + 0.08); bk.rotation.x = -0.35; g.add(bk); }
      if (key === 'R' && c.scroll) { const sc = mesh(new T.CylinderGeometry(0.06, 0.06, 0.55, 10), marble, hand.x, hand.y, hand.z); sc.rotation.z = 1.2; g.add(sc); }
    }
    g.scale.setScalar(1.55);
    return g;
  }

  // ---------- idea sculptures (each returns a Group, may push an update fn) ----------
  const rnd = (a, b) => a + Math.random() * (b - a);
  const anim = fn => animated.push(fn);
  const IDEAS = {
    armillary() { const g = new T.Group(); [0, 1, 2, 3].forEach(i => { const r = mesh(new T.TorusGeometry(1.2, 0.03, 8, 64), gold); r.rotation.set(i * 0.8, i * 0.5, 0); g.add(r); anim(t => { r.rotation.y += 0.004 * (i + 1); r.rotation.x += 0.002 * i; }); }); g.add(mesh(new T.SphereGeometry(0.35, 20, 16), glow(0xffe08a, 1.2))); return g; },
    apeiron() { const g = new T.Group(), geo = new T.IcosahedronGeometry(1, 3), base = geo.attributes.position.array.slice(); const m = mesh(geo, new T.MeshStandardMaterial({ color: 0xd8c9a8, transparent: true, opacity: 0.5, roughness: 0.9, flatShading: true })); g.add(m);
      g.add(mesh(new T.SphereGeometry(0.5, 16, 12), glow(0xfff2c8, 0.7)));
      anim(t => { const p = geo.attributes.position; for (let i = 0; i < p.count; i++) { const x = base[i * 3], y = base[i * 3 + 1], z = base[i * 3 + 2], k = 1 + 0.18 * Math.sin(t * 1.3 + x * 3 + y * 2 + z * 2.4); p.setXYZ(i, x * k, y * k, z * k); } p.needsUpdate = true; geo.computeVertexNormals(); m.rotation.y = t * 0.2; }); return g; },
    tortoise() { const g = new T.Group(), c = 0x6b8e3c; const sh = mesh(new T.SphereGeometry(1, 20, 12, 0, 6.283, 0, 1.6), new T.MeshStandardMaterial({ color: c, roughness: 0.7 })); sh.scale.set(1, 0.65, 0.8); g.add(sh);
      g.add(mesh(new T.SphereGeometry(0.22, 12, 10), new T.MeshStandardMaterial({ color: 0x8aa84e }), 1.05, 0.05, 0));
      [[-0.5, -0.5], [0.5, -0.5], [-0.5, 0.5], [0.5, 0.5]].forEach(p => g.add(mesh(new T.SphereGeometry(0.17, 8, 6), new T.MeshStandardMaterial({ color: 0x8aa84e }), p[0], -0.3, p[1] * 0.8)));
      anim(t => { g.position.x = Math.sin(t * 0.5) * 0.05; g.rotation.y = Math.sin(t * 0.3) * 0.4; }); return g; },
    stele() { const g = new T.Group(), tex = canvasTex(128, 256, (c, w, h) => { c.fillStyle = '#2a2420'; c.fillRect(0, 0, w, h); c.fillStyle = '#d9c9a0'; for (let r = 0; r < 18; r++) for (let k = 0; k < 6; k++) if (Math.random() > 0.2) { c.save(); c.translate(14 + k * 18, 60 + r * 10); c.rotate(Math.random() * 3); c.fillRect(0, 0, 8, 2); c.restore(); } });
      const s = mesh(new T.BoxGeometry(0.9, 1.7, 0.3), new T.MeshStandardMaterial({ map: tex, roughness: 0.6 })); g.add(s); g.add(mesh(new T.CylinderGeometry(0.45, 0.45, 0.3, 20, 1, false, 0, 3.1416), glow(0xd9c9a0, 0.15)).rotateX(Math.PI / 2).translateY(0).translateZ(0)); g.children[1].position.set(0, 0.85, 0); g.children[1].rotation.set(0, 1.57, 0); anim(t => { g.rotation.y = Math.sin(t * 0.4) * 0.5; }); return g; },
    rings() { const g = new T.Group(), cols = [0xe5b84a, 0xd0724a, 0x6aa0d0, 0x7ac58a]; cols.forEach((c, i) => { const r = mesh(new T.TorusGeometry(0.35 + i * 0.28, 0.035, 8, 56), glow(c, 0.8)); r.rotation.x = Math.PI / 2; g.add(r); anim(t => { r.rotation.z = t * (0.4 - i * 0.1); r.position.y = Math.sin(t + i) * 0.05; }); }); g.add(mesh(new T.SphereGeometry(0.16, 12, 10), glow(0xffffff, 1))); return g; },
    wheel() { const g = new T.Group(), w = new T.Group(); w.add(mesh(new T.TorusGeometry(1, 0.06, 10, 48), gold)); w.add(mesh(new T.SphereGeometry(0.18, 12, 10), gold)); for (let i = 0; i < 8; i++) { const s = mesh(new T.CylinderGeometry(0.03, 0.03, 1, 6), gold); s.position.set(Math.cos(i * 0.785) * 0.5, Math.sin(i * 0.785) * 0.5, 0); s.rotation.z = i * 0.785 + 1.5708; w.add(s); } g.add(w); anim(t => { w.rotation.z = -t * 0.4; g.rotation.y = Math.sin(t * 0.3) * 0.5; }); return g; },
    forms() { const g = new T.Group(), a = mesh(new T.DodecahedronGeometry(1), wire(0xa8d0ff)), b = mesh(new T.OctahedronGeometry(0.6), glow(0xffd58a, 0.8)), c = mesh(new T.IcosahedronGeometry(0.85), wire(0xffffff)); g.add(a, b, c); anim(t => { a.rotation.set(t * 0.2, t * 0.3, 0); c.rotation.set(-t * 0.25, t * 0.15, 0); b.rotation.y = t * 0.6; }); return g; },
    causes() { const g = new T.Group(), cols = [0xd0724a, 0x6aa0d0, 0xe5b84a, 0x7ac58a]; g.add(mesh(new T.SphereGeometry(0.4, 16, 12), glass(0xffffff, 0.45))); cols.forEach((c, i) => { const s = mesh(new T.SphereGeometry(0.17, 12, 10), glow(c, 0.9)); g.add(s); anim(t => { const a = t * 0.8 + i * 1.5708; s.position.set(Math.cos(a) * (0.8 + i * 0.12), Math.sin(t * 0.6 + i) * 0.35, Math.sin(a) * (0.8 + i * 0.12)); }); }); return g; },
    garden() { const g = new T.Group(); g.add(mesh(new T.SphereGeometry(0.28, 16, 12), glow(0x9be0a8, 0.9))); for (let i = 0; i < 3; i++) { const r = mesh(new T.TorusGeometry(1, 0.02, 6, 48), glow(0x9be0a8, 0.5)); r.rotation.x = Math.PI / 2; g.add(r); anim(t => { const k = (t * 0.25 + i / 3) % 1; r.scale.setScalar(0.3 + k * 1.2); r.material.opacity = 1 - k; r.material.transparent = true; r.position.y = -0.4; }); } anim(t => { g.children[0].position.y = Math.sin(t * 0.8) * 0.1; }); return g; },
    perfect() { const g = new T.Group(); g.add(mesh(new T.SphereGeometry(0.7, 28, 20), gold)); const h = mesh(new T.TorusGeometry(1.0, 0.02, 6, 60), glow(0xffe08a, 1)); g.add(h); const h2 = h.clone(); h2.rotation.y = 1.5708; g.add(h2); g.add(new T.PointLight(0xffe08a, 0.8, 8)); anim(t => { h.rotation.x = t * 0.5; h2.rotation.x = -t * 0.4; }); return g; },
    lamp() { const g = new T.Group(); const f = mesh(new T.ConeGeometry(0.28, 0.9, 12), glow(0xff8a2a, 1.4)); f.position.set(-0.55, 0.1, 0); g.add(f); g.add(mesh(new T.ConeGeometry(0.14, 0.6, 12), glow(0xffe08a, 1.6), -0.55, 0, 0)); const cot = mesh(new T.SphereGeometry(0.45, 14, 10), new T.MeshStandardMaterial({ color: 0xffffff, roughness: 1 })); cot.position.set(0.7, -0.15, 0); g.add(cot); const a = mesh(new T.TorusGeometry(0.28, 0.02, 6, 20, 3.14), glow(0xffe08a, 0.6)); a.position.set(0.1, 0.6, 0); a.rotation.z = 0; g.add(a); anim(t => { f.scale.set(1 + Math.sin(t * 9) * 0.06, 1 + Math.sin(t * 7) * 0.1, 1); }); return g; },
    knot() { const g = new T.Group(), k = mesh(new T.TorusKnotGeometry(0.7, 0.2, 120, 14, 3, 2), new T.MeshStandardMaterial({ color: 0x4a78d0, metalness: 0.7, roughness: 0.25 })); g.add(k); anim(t => { k.rotation.set(t * 0.3, t * 0.4, 0); }); return g; },
    vitruvian() { const g = new T.Group(); g.add(mesh(new T.TorusGeometry(1, 0.025, 8, 64), gold)); const sq = new T.LineSegments(new T.EdgesGeometry(new T.BoxGeometry(1.5, 1.5, 0.02)), new T.LineBasicMaterial({ color: 0xffd58a })); g.add(sq); g.add(new T.LineSegments(new T.EdgesGeometry(new T.BoxGeometry(0.05, 1.9, 0.02)), new T.LineBasicMaterial({ color: 0xffd58a }))); g.add(new T.LineSegments(new T.EdgesGeometry(new T.BoxGeometry(1.9, 0.05, 0.02)), new T.LineBasicMaterial({ color: 0xffd58a }))); anim(t => { g.rotation.y = t * 0.5; }); return g; },
    crown() { const g = new T.Group(); g.add(mesh(new T.CylinderGeometry(0.6, 0.55, 0.4, 20, 1, true), gold)); for (let i = 0; i < 7; i++) { const a = i / 7 * 6.283; g.add(mesh(new T.ConeGeometry(0.1, 0.35, 8), gold, Math.cos(a) * 0.58, 0.35, Math.sin(a) * 0.58)); g.add(mesh(new T.SphereGeometry(0.07, 8, 6), glow(0xc0485a, 1), Math.cos(a) * 0.58, 0.55, Math.sin(a) * 0.58)); } anim(t => { g.rotation.y = t * 0.5; g.position.y = Math.sin(t) * 0.05; }); return g; },
    hourglass() { const g = new T.Group(), gm = glass(0xcfe3ff, 0.35); g.add(mesh(new T.ConeGeometry(0.55, 0.85, 20, 1, true), gm, 0, -0.45, 0)); const up = mesh(new T.ConeGeometry(0.55, 0.85, 20, 1, true), gm, 0, 0.45, 0); up.rotation.x = Math.PI; g.add(up); const s = mesh(new T.SphereGeometry(0.1, 8, 6), glow(0xe5b84a, 1)); g.add(s); [-1, 1].forEach(sy => g.add(mesh(new T.CylinderGeometry(0.62, 0.62, 0.06, 20), gold, 0, sy * 0.9, 0))); anim(t => { s.position.y = 0.4 - ((t * 0.5) % 1) * 0.8; }); return g; },
    contract() { const g = new T.Group(); const n = 9; for (let i = 0; i < n; i++) { const a = i / n * 6.283, s = mesh(new T.SphereGeometry(0.14, 10, 8), glow(0xf0a860, 0.8), Math.cos(a), 0, Math.sin(a)); g.add(s); } const r = mesh(new T.TorusGeometry(1, 0.025, 6, 60), glow(0xf0a860, 0.5)); r.rotation.x = Math.PI / 2; g.add(r); g.add(mesh(new T.SphereGeometry(0.3, 14, 10), glow(0xffffff, 1))); anim(t => { g.rotation.y = t * 0.4; g.children[g.children.length - 1].scale.setScalar(1 + Math.sin(t * 2) * 0.12); }); return g; },
    stars() { const g = new T.Group(), n = 500, p = new Float32Array(n * 3); for (let i = 0; i < n; i++) { const u = Math.random() * 2 - 1, a = Math.random() * 6.283, s = Math.sqrt(1 - u * u), r = 1.2 + Math.random() * 0.2; p[i * 3] = Math.cos(a) * s * r; p[i * 3 + 1] = u * r; p[i * 3 + 2] = Math.sin(a) * s * r; } const geo = new T.BufferGeometry(); geo.setAttribute('position', new T.BufferAttribute(p, 3)); const pts = new T.Points(geo, new T.PointsMaterial({ color: 0xffffff, size: 0.06 })); g.add(pts); const cube = mesh(new T.BoxGeometry(0.7, 0.7, 0.7), glow(0xffd58a, 0.5)); cube.material.transparent = true; cube.material.opacity = 0.85; g.add(cube); anim(t => { pts.rotation.y = t * 0.1; cube.rotation.set(t * 0.3, t * 0.4, 0); }); return g; },
    dialectic() { const g = new T.Group(), a = mesh(new T.SphereGeometry(0.3, 16, 12), glow(0xd04a4a, 0.9)), b = mesh(new T.SphereGeometry(0.3, 16, 12), glow(0x4a6ad0, 0.9)), c = mesh(new T.SphereGeometry(0.4, 18, 14), glow(0xa04ad0, 1)); g.add(a, b, c); anim(t => { const k = (Math.sin(t * 0.8) + 1) / 2, r = 1.0 * k + 0.1; a.position.set(Math.cos(t) * r, 0, Math.sin(t) * r); b.position.set(-Math.cos(t) * r, 0, -Math.sin(t) * r); c.scale.setScalar(0.5 + (1 - k) * 0.9); }); return g; },
    grin() { const g = new T.Group(); const s = mesh(new T.TorusGeometry(0.9, 0.07, 10, 40, 3.1416), glow(0xff6aa8, 1)); s.rotation.z = Math.PI; g.add(s); for (const x of [-0.4, 0.4]) { const e = mesh(new T.SphereGeometry(1, 12, 10), glow(0xffd1e3, 1), x, 0.5, 0); e.scale.set(0.1, 0.18, 0.1); g.add(e); } anim(t => { g.rotation.y = Math.sin(t * 0.7) * 0.5; g.position.y = Math.sin(t) * 0.05; }); return g; },
    hotel() { const g = new T.Group(); for (let i = 0; i < 8; i++) { const m = glow(0xe5b84a, 0.7 - i * 0.07); m.transparent = true; m.opacity = 1 - i * 0.12; g.add(mesh(new T.BoxGeometry(0.4, 0.5, 0.5), m, -1.5 + i * 0.5, 0, 0)); } anim(t => { g.rotation.y = Math.sin(t * 0.5) * 0.4; }); return g; },
    construct() { const g = new T.Group(); g.add(new T.LineSegments(new T.EdgesGeometry(new T.BoxGeometry(1.6, 1.6, 1.6)), new T.LineBasicMaterial({ color: 0x9fd6ff }))); const cubes = []; for (let x = 0; x < 3; x++) for (let y = 0; y < 3; y++) for (let z = 0; z < 3; z++) { const c = mesh(new T.BoxGeometry(0.46, 0.46, 0.46), glow(0x7ac5ff, 0.7), -0.52 + x * 0.52, -0.52 + y * 0.52, -0.52 + z * 0.52); c.visible = false; g.add(c); cubes.push(c); } anim(t => { const n = Math.floor((t * 3) % 40); cubes.forEach((c, i) => c.visible = i < n); g.rotation.y = t * 0.3; }); return g; },
    recur() { const g = new T.Group(), r = mesh(new T.TorusGeometry(1, 0.05, 8, 64), glow(0xd09a4a, 0.5)); g.add(r); const orbs = []; for (let i = 0; i < 8; i++) { const o = mesh(new T.SphereGeometry(0.1, 10, 8), glow(0xffe08a, 1)); g.add(o); orbs.push(o); } anim(t => { orbs.forEach((o, i) => { const a = t * 0.8 + i * 0.785; o.position.set(Math.cos(a), Math.sin(a), 0); }); r.rotation.z = -t * 0.1; g.rotation.y = Math.sin(t * 0.3) * 0.6; }); return g; },
    iceberg() { const g = new T.Group(); g.add(mesh(new T.ConeGeometry(0.35, 0.5, 6), new T.MeshStandardMaterial({ color: 0xffffff, flatShading: true }), 0, 0.3, 0)); const lo = mesh(new T.ConeGeometry(1.0, 1.5, 7), new T.MeshStandardMaterial({ color: 0x4a6a9a, flatShading: true, transparent: true, opacity: 0.85 }), 0, -0.7, 0); lo.rotation.x = Math.PI; g.add(lo); const w = mesh(new T.CylinderGeometry(1.4, 1.4, 0.02, 32), glass(0x6aa0d0, 0.35)); g.add(w); anim(t => { g.rotation.y = t * 0.25; }); return g; },
    spacetime() { const g = new T.Group(), geo = new T.PlaneGeometry(2.6, 2.6, 26, 26), p = geo.attributes.position; for (let i = 0; i < p.count; i++) { const x = p.getX(i), y = p.getY(i), r = Math.hypot(x, y); p.setZ(i, -0.9 / (r + 0.55)); } geo.computeVertexNormals(); const pl = mesh(geo, wire(0x7ac5ff)); pl.rotation.x = -1.2; g.add(pl); const sun = mesh(new T.SphereGeometry(0.28, 16, 12), glow(0xffd24a, 1.2)); sun.position.y = -0.2; g.add(sun); const pt = mesh(new T.SphereGeometry(0.09, 8, 6), glow(0xffffff, 1)); g.add(pt); anim(t => { const a = t * 1.1, r = 0.95; pt.position.set(Math.cos(a) * r, -0.35 + Math.sin(a) * r * Math.sin(-1.2) * -0.0 + Math.sin(a) * 0.35, Math.sin(a) * r * 0.55); g.rotation.y = t * 0.1; }); return g; },
    clearing() { const g = new T.Group(); g.add(mesh(new T.BoxGeometry(0.7, 0.45, 0.6), new T.MeshStandardMaterial({ color: 0x8a5a2e }), 0, -0.3, 0)); const roof = mesh(new T.ConeGeometry(0.62, 0.4, 4), new T.MeshStandardMaterial({ color: 0x5a3a1c }), 0, 0.05, 0); roof.rotation.y = Math.PI / 4; g.add(roof); for (let i = 0; i < 8; i++) { const a = i / 8 * 6.283, r = 1.0 + (i % 2) * 0.2; g.add(mesh(new T.ConeGeometry(0.2, 0.8, 6), new T.MeshStandardMaterial({ color: 0x2f5a3a }), Math.cos(a) * r, -0.2, Math.sin(a) * r)); } const l = mesh(new T.CylinderGeometry(0.1, 0.9, 1.8, 20, 1, true), new T.MeshBasicMaterial({ color: 0xffe9a8, transparent: true, opacity: 0.18, blending: T.AdditiveBlending, depthWrite: false }), 0, 0.8, 0); g.add(l); anim(t => { g.rotation.y = t * 0.25; }); return g; },
    cage() { const g = new T.Group(); g.add(new T.LineSegments(new T.EdgesGeometry(new T.BoxGeometry(1.0, 1.0, 1.0)), new T.LineBasicMaterial({ color: 0xc0c0c0 }))); const s = mesh(new T.SphereGeometry(0.25, 14, 10), glow(0xff7a4a, 1)); g.add(s); anim(t => { const k = (Math.sin(t * 0.6) + 1) / 2; s.position.set(k * 1.5 * 0.9, Math.sin(t * 2) * 0.12 + k * 0.4, 0); g.rotation.y = t * 0.2; }); return g; },
    eye() { const g = new T.Group(); g.add(mesh(new T.SphereGeometry(0.8, 28, 20), new T.MeshStandardMaterial({ color: 0xf6f2ea, roughness: 0.25 }))); const iris = mesh(new T.CircleGeometry(0.38, 28), new T.MeshStandardMaterial({ color: 0x3a82c4, emissive: 0x143a6a, roughness: 0.3 }), 0, 0, 0.806); const pup = mesh(new T.CircleGeometry(0.16, 20), new T.MeshBasicMaterial({ color: 0 }), 0, 0, 0.81); const look = new T.Group(); look.add(iris, pup); g.add(look); anim(t => { look.rotation.y = Math.sin(t * 0.9) * 0.45; look.rotation.x = Math.sin(t * 0.6) * 0.25; g.rotation.y = Math.sin(t * 0.3) * 0.4; }); return g; },
    rhizome() { const g = new T.Group(), n = 38, pts = []; for (let i = 0; i < n; i++) pts.push(new T.Vector3(rnd(-1, 1), rnd(-0.8, 0.8), rnd(-1, 1))); const seg = []; pts.forEach((p, i) => { pts.map((q, j) => [p.distanceTo(q), j]).sort((a, b) => a[0] - b[0]).slice(1, 4).forEach(([d, j]) => { seg.push(p.x, p.y, p.z, pts[j].x, pts[j].y, pts[j].z); }); }); const geo = new T.BufferGeometry(); geo.setAttribute('position', new T.Float32BufferAttribute(seg, 3)); g.add(new T.LineSegments(geo, new T.LineBasicMaterial({ color: 0x7ae0a0 }))); pts.forEach(p => g.add(mesh(new T.SphereGeometry(0.05, 6, 5), glow(0xb8ffd0, 1), p.x, p.y, p.z))); anim(t => { g.rotation.y = t * 0.2; g.rotation.x = Math.sin(t * 0.3) * 0.2; }); return g; },
    panopticon() { const g = new T.Group(); for (let i = 0; i < 14; i++) { const a = i / 14 * 6.283, c = mesh(new T.BoxGeometry(0.28, 0.5, 0.05), new T.MeshStandardMaterial({ color: 0x777777 }), Math.cos(a) * 1.0, 0, Math.sin(a) * 1.0); c.rotation.y = -a + 1.5708; g.add(c); g.add(mesh(new T.SphereGeometry(0.06, 6, 5), glow(0xffe08a, 0.7), Math.cos(a) * 0.93, -0.05, Math.sin(a) * 0.93)); } g.add(mesh(new T.CylinderGeometry(0.16, 0.2, 1.2, 12), stoneDark, 0, 0.1, 0)); const beam = mesh(new T.ConeGeometry(0.6, 1.1, 14, 1, true), new T.MeshBasicMaterial({ color: 0xffe9a8, transparent: true, opacity: 0.35, blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide }), 0.55, 0.45, 0); beam.rotation.z = -1.5708; const pivot = new T.Group(); pivot.add(beam); g.add(pivot); anim(t => { pivot.rotation.y = t * 1.2; }); return g; },
    nothing() { const g = new T.Group(); g.add(mesh(new T.BoxGeometry(1.5, 1.5, 1.5), glass(0xffffff, 0.08))); g.add(new T.LineSegments(new T.EdgesGeometry(new T.BoxGeometry(1.5, 1.5, 1.5)), new T.LineBasicMaterial({ color: 0xffffff }))); anim(t => { g.rotation.y = t * 0.2; }); return g; },
    chaos() { const g = new T.Group(), n = 7000, p = new Float32Array(n * 3), col = new Float32Array(n * 3); let x = 0.1, y = 0, z = 0; const dt = 0.006; for (let i = 0; i < n; i++) { const dx = 10 * (y - x), dy = x * (28 - z) - y, dz = x * y - 8 / 3 * z; x += dx * dt; y += dy * dt; z += dz * dt; p[i * 3] = x * 0.045; p[i * 3 + 1] = (z - 25) * 0.045; p[i * 3 + 2] = y * 0.045; const c = new T.Color().setHSL(i / n * 0.8, 0.8, 0.6); col[i * 3] = c.r; col[i * 3 + 1] = c.g; col[i * 3 + 2] = c.b; } const geo = new T.BufferGeometry(); geo.setAttribute('position', new T.BufferAttribute(p, 3)); geo.setAttribute('color', new T.BufferAttribute(col, 3)); g.add(new T.Line(geo, new T.LineBasicMaterial({ vertexColors: true }))); anim(t => { g.rotation.y = t * 0.3; }); return g; },
    mind() { const g = new T.Group(); g.add(mesh(new T.SphereGeometry(1, 28, 20), glass(0xaad0ff, 0.2))); const o = mesh(new T.SphereGeometry(0.35, 20, 16), glow(0xfff0b0, 1.4)); g.add(o); g.add(new T.PointLight(0xfff0b0, 0.7, 7)); for (let i = 0; i < 3; i++) { const r = mesh(new T.TorusGeometry(0.55 + i * 0.12, 0.012, 6, 48), glow(0xfff0b0, 0.6)); g.add(r); anim(t => { r.rotation.set(t * 0.4 + i, t * 0.3 + i * 2, 0); }); } anim(t => { o.scale.setScalar(1 + Math.sin(t * 1.5) * 0.15); }); return g; },
    logic() { const g = new T.Group(), cols = [0xd04a4a, 0x4ad04a, 0x4a6ad0]; cols.forEach((c, i) => { const a = i / 3 * 6.283 + 1.57; const r = mesh(new T.TorusGeometry(0.62, 0.035, 8, 48), glow(c, 0.9), Math.cos(a) * 0.4, Math.sin(a) * 0.4 - 0.1, 0); g.add(r); }); g.add(labelSprite('∴', 0.5, '#fff')); g.children[3].scale.set(2, 0.5, 1); anim(t => { g.rotation.y = Math.sin(t * 0.6) * 0.7; }); return g; },
    truth() { const g = new T.Group(); const pr = mesh(new T.CylinderGeometry(0.6, 0.6, 1.2, 3), glass(0xe8f4ff, 0.5)); pr.rotation.z = Math.PI / 2; g.add(pr); g.add(new T.LineSegments(new T.EdgesGeometry(pr.geometry), new T.LineBasicMaterial({ color: 0xffffff })).translateX(0)); g.children[1].rotation.z = Math.PI / 2; const cols = [0xff4a4a, 0xff9a4a, 0xffe04a, 0x4aff7a, 0x4aa0ff, 0x8a4aff]; cols.forEach((c, i) => { const b = mesh(new T.BoxGeometry(1.6, 0.05, 0.05), glow(c, 1), 1.4, -0.1 + (i - 2.5) * 0.12, 0); b.rotation.z = (i - 2.5) * 0.12; g.add(b); }); g.add(mesh(new T.BoxGeometry(1.2, 0.05, 0.05), glow(0xffffff, 1), -1.2, 0, 0)); anim(t => { g.rotation.y = t * 0.3; }); return g; },
    meaning() { const g = new T.Group(); const pts = []; for (let i = 0; i <= 80; i++) { const a = i * 0.28; pts.push(new T.Vector3(Math.cos(a) * (0.9 - i * 0.004), -0.9 + i * 0.024, Math.sin(a) * (0.9 - i * 0.004))); } g.add(mesh(new T.TubeGeometry(new T.CatmullRomCurve3(pts), 160, 0.035, 6), glow(0xb08aff, 0.9))); const q = labelSprite('?', 1.6, '#ffe08a'); q.scale.set(1.6, 1.6, 1); q.material.map.repeat.set(0.1, 1); q.material.map.offset.set(0.45, 0); g.add(q); q.position.y = 1.4; anim(t => { g.rotation.y = t * 0.4; q.position.y = 1.2 + Math.sin(t * 1.5) * 0.1; }); return g; },
    justice() { const g = new T.Group(); g.add(mesh(new T.CylinderGeometry(0.05, 0.08, 1.6, 8), gold, 0, -0.2, 0)); const beam = new T.Group(); beam.add(mesh(new T.BoxGeometry(2, 0.06, 0.08), gold)); for (const sx of [-1, 1]) { const pan = mesh(new T.CylinderGeometry(0.45, 0.2, 0.1, 16), gold, sx * 0.95, -0.7, 0); beam.add(pan); beam.add(new T.LineSegments(new T.BufferGeometry().setFromPoints([new T.Vector3(sx * 0.95, 0, 0), new T.Vector3(sx * 0.6, -0.65, 0), new T.Vector3(sx * 0.95, 0, 0), new T.Vector3(sx * 1.3, -0.65, 0)]), new T.LineBasicMaterial({ color: 0xd4af37 }))); } beam.position.y = 0.6; g.add(beam); anim(t => { beam.rotation.z = Math.sin(t * 0.9) * 0.15; g.rotation.y = Math.sin(t * 0.3) * 0.4; }); return g; },
    freedom() { const g = new T.Group(), m = new T.MeshStandardMaterial({ color: 0xb0b0b8, metalness: 0.9, roughness: 0.3 }); for (let i = 0; i < 5; i++) { const l = mesh(new T.TorusGeometry(0.25, 0.07, 8, 20), m, -1.2 + i * 0.5, 0, 0); if (i % 2) l.rotation.y = Math.PI / 2; g.add(l); anim(t => { if (i >= 3) { const s = (i - 2) * 0.12 * (Math.sin(t) + 1.2); l.position.y = s * 1.2 - 0.0; l.position.x = -1.2 + i * 0.5 + s; l.rotation.z = s; } }); } anim(t => { g.rotation.y = Math.sin(t * 0.4) * 0.5; }); return g; },
  };

  // ---------- world construction ----------
  const wallMats = HALLS.map(h => new T.MeshStandardMaterial({ color: new T.Color(h.tint).multiplyScalar(0.35).add(new T.Color(0x303038)), roughness: 0.9 }));
  const colliders = [];            // circles {x,z,r}
  const exhibits = [];             // runtime exhibit records
  const totalZ = -6 * L;

  HALLS.forEach((h, i) => {
    const z0 = -i * L, c = zc(i);
    const fl = mesh(new T.PlaneGeometry(W, L), new T.MeshStandardMaterial({ map: floorTex, color: h.floor, roughness: 0.35, metalness: 0.05 }), 0, 0, c); fl.rotation.x = -Math.PI / 2; scene.add(fl);
    const ce = mesh(new T.PlaneGeometry(W, L), new T.MeshStandardMaterial({ map: starTex, emissiveMap: starTex, emissive: 0xffffff, emissiveIntensity: 0.6, color: 0x222233 }), 0, H, c); ce.rotation.x = Math.PI / 2; scene.add(ce);
    for (const sx of [-1, 1]) {
      const wl = mesh(new T.BoxGeometry(0.6, H, L), wallMats[i], sx * (W / 2 + 0.3), H / 2, c); scene.add(wl);
      for (let k = 0; k < 5; k++) { const col = mesh(new T.CylinderGeometry(0.45, 0.5, H, 14), marble, sx * (W / 2 - 0.6), H / 2, c - L / 2 + 3 + k * 6); scene.add(col); }
      const li = new T.PointLight(0xffe6c0, 0.8, 38, 1.4); li.position.set(sx * 7, 8.5, c); scene.add(li);
    }
    // gold cornice
    scene.add(mesh(new T.BoxGeometry(W, 0.3, 0.3), gold, 0, H - 0.2, z0 - L + 0.2));
    // dividing wall at far end with a door gap (and end wall for last hall)
    const wz = z0 - L;
    const last = i === HALLS.length - 1;
    const gap = last ? 0 : DOOR;
    const segW = W / 2 - gap;
    for (const sx of [-1, 1]) scene.add(mesh(new T.BoxGeometry(segW, H, 0.8), wallMats[i], sx * (gap + segW / 2), H / 2, wz));
    if (!last) {
      scene.add(mesh(new T.BoxGeometry(gap * 2, H - 6, 0.8), wallMats[i], 0, 6 + (H - 6) / 2, wz));
      for (const sx of [-1, 1]) scene.add(mesh(new T.CylinderGeometry(0.4, 0.4, 6, 12), gold, sx * gap, 3, wz + 0.5));
      const sign = labelSprite(HALLS[i + 1].name, 1.3, '#ffe9b0'); sign.position.set(0, 7.2, wz + 0.6); scene.add(sign);
      const sub = labelSprite(HALLS[i + 1].sub, 0.6, '#cfc7b0'); sub.position.set(0, 6.3, wz + 0.6); scene.add(sub);
    } else {
      const t = labelSprite('Keep asking.', 2, '#ffe9b0'); t.position.set(0, 6, wz + 0.6); scene.add(t);
    }
  });
  // north wall of the atrium
  scene.add(mesh(new T.BoxGeometry(W, H, 0.8), wallMats[0], 0, H / 2, 0.4));
  { const t = labelSprite('HALL OF THOUGHT', 2.2, '#ffe9b0'); t.position.set(0, 7.5, 0.0); t.position.z = -0.1; scene.add(t); const s = labelSprite('walk forward through the history of ideas', 0.6, '#cfc7b0'); s.position.set(0, 6.2, -0.1); scene.add(s); }

  // atrium bookshelves with real titles
  (function shelves() {
    const geo = new T.BoxGeometry(0.14, 0.9, 0.62);
    for (const sx of [-1, 1]) {
      scene.add(mesh(new T.BoxGeometry(0.9, 6.2, L - 6), stoneDark, sx * (W / 2 - 1.0), 3.1, zc(0) - 0.0));
      for (let row = 0; row < 4; row++) for (let k = 0; k < 22; k++) {
        const t = VSI_SHELF[(k + row * 5 + (sx > 0 ? 7 : 0)) % VSI_SHELF.length];
        const m = coverMat(t + ' : A Very Short Introduction', true);
        const b = new T.Mesh(geo, sx < 0 ? [m.front, m.spine, m.paper, m.paper, m.paper, m.paper] : [m.spine, m.front, m.paper, m.paper, m.paper, m.paper]);
        b.position.set(sx * (W / 2 - 1.5), 1.1 + row * 1.4, zc(0) - (L - 6) / 2 + 0.6 + k * 0.62); scene.add(b);
      }
    }
    const s = labelSprite('A Very Short Introduction to… (from the folder)', 0.5, '#cfc7b0'); s.position.set(-(W / 2 - 2), 6.4, zc(0)); s.rotation.y = Math.PI / 2; scene.add(s);
    const s2 = s.clone(); s2.position.x *= -1; scene.add(s2);
  })();

  // exhibits
  const perHall = HALLS.map((_, i) => EXHIBITS.filter(e => e.hall === i));
  perHall.forEach((list, hi) => {
    const c = zc(hi), n = list.length;
    list.forEach((ex, k) => {
      let x, z, rotY;
      if (ex.center) { x = 0; z = c; rotY = 0; }
      else if (ex.ring) { const a = k / n * 6.283 + 0.4, R = 9; x = Math.cos(a) * R; z = c + Math.sin(a) * R; rotY = Math.atan2(-x, c - z); }
      else { const pairs = Math.ceil(n / 2), p = Math.floor(k / 2); z = c + ((pairs - 1) / 2 - p) * 6.5; x = k % 2 ? 9.2 : -9.2; rotY = k % 2 ? -Math.PI / 2 : Math.PI / 2; }
      const root = new T.Group(); root.position.set(x, 0, z); root.rotation.y = rotY; scene.add(root);
      const plH = ex.fig ? 1.1 : 1.0;
      root.add(mesh(new T.BoxGeometry(2.6, plH, 2.6), marble, 0, plH / 2, 0));
      root.add(mesh(new T.BoxGeometry(3.0, 0.15, 3.0), stoneDark, 0, 0.07, 0));
      root.add(mesh(new T.BoxGeometry(2.8, 0.1, 2.8), gold, 0, plH + 0.04, 0));
      // plaque
      const plaque = new T.Mesh(new T.PlaneGeometry(2.2, 0.6), new T.MeshBasicMaterial({ map: canvasTex(512, 140, (g, w, h) => { g.fillStyle = '#1a1612'; g.fillRect(0, 0, w, h); g.strokeStyle = '#d4af37'; g.lineWidth = 4; g.strokeRect(6, 6, w - 12, h - 12); g.fillStyle = '#f3e6bd'; g.font = '600 44px Georgia'; g.textAlign = 'center'; g.fillText(ex.name.length > 24 ? ex.name.slice(0, 24) : ex.name, w / 2, 62); g.font = 'italic 26px Georgia'; g.fillStyle = '#d4af37'; g.fillText(ex.years.length > 36 ? ex.years.slice(0, 36) : ex.years, w / 2, 106); }) }));
      plaque.position.set(0, plH * 0.5, 1.32); root.add(plaque);
      let topY = plH + 0.1;
      if (ex.fig) { const s = makeStatue(ex.fig); s.position.y = topY; root.add(s); }
      const idea = IDEAS[ex.idea](); const sc = ex.fig ? 1.2 : 1.6; idea.scale.setScalar(sc);
      idea.position.set(0, ex.fig ? 6.9 : plH + 2.2, 0); if (ex.fig) idea.rotation.y = 0; root.add(idea);
      const tag = labelSprite(ex.tag, 0.55, '#ffe9b0'); tag.position.set(0, ex.fig ? 8.7 : plH + 4.1, 0); root.add(tag);
      // light pool
      const pool = mesh(new T.CircleGeometry(2.4, 32), new T.MeshBasicMaterial({ color: HALLS[hi].tint, transparent: true, opacity: 0.25, blending: T.AdditiveBlending, depthWrite: false }), 0, 0.02, 0); pool.rotation.x = -Math.PI / 2; root.add(pool);
      const beam = mesh(new T.CylinderGeometry(0.9, 1.9, 9, 24, 1, true), new T.MeshBasicMaterial({ color: HALLS[hi].tint, transparent: true, opacity: 0.07, blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide }), 0, 4.5, 0); root.add(beam);
      // books on a table in front of the plinth (toward the aisle / centre)
      const tbl = bookTable(ex.books); tbl.position.set(0, 0, 3.0); root.add(tbl);
      colliders.push({ x, z, r: 1.9 });
      const tx = x + Math.sin(rotY) * 3.0, tz = z + Math.cos(rotY) * 3.0; colliders.push({ x: tx, z: tz, r: 1.1 });
      exhibits.push({ ex, x, z, hall: hi, tx, tz });
    });
  });
  // atrium armillary sits on a taller plinth already; add a ceiling oculus feel
  scene.add(mesh(new T.CircleGeometry(4.5, 40), new T.MeshBasicMaterial({ color: 0xc9a24a, transparent: true, opacity: 0.18, blending: T.AdditiveBlending }), 0, 0.03, zc(0)).rotateX(-Math.PI / 2));

  // ---------- controls ----------
  const keys = {}; let yaw = 0, pitch = 0, locked = false, dragging = false;
  const pos = new T.Vector3(0, 1.75, -4), vel = new T.Vector3();
  const overlay = document.getElementById('overlay'), card = document.getElementById('card'), hallEl = document.getElementById('hall');
  function tp(i) { pos.set(0, 1.75, zc(i) + L / 2 - 3); yaw = 0; pitch = 0; vel.set(0, 0, 0); }
  window.__tp = (i, y) => { tp(i); if (y !== undefined) yaw = y; };
  window.__look = (y, p) => { yaw = y; pitch = p; }; window.__at = (x, z) => pos.set(x, 1.75, z);
  addEventListener('keydown', e => { keys[e.code] = true; if (/^Digit[1-6]$/.test(e.code)) tp(+e.code.slice(5) - 1); if (e.code === 'Escape') overlay.style.display = 'flex'; });
  addEventListener('keyup', e => keys[e.code] = false);
  function enter() { overlay.style.display = 'none'; if (renderer.domElement.requestPointerLock) renderer.domElement.requestPointerLock(); }
  overlay.addEventListener('click', enter);
  renderer.domElement.addEventListener('click', () => { if (!locked && overlay.style.display === 'none' && renderer.domElement.requestPointerLock) renderer.domElement.requestPointerLock(); });
  document.addEventListener('pointerlockchange', () => { locked = document.pointerLockElement === renderer.domElement; if (!locked && !dragging) overlay.style.display = overlay.dataset.keep === '1' ? 'none' : 'flex'; });
  addEventListener('mousemove', e => { if (locked || dragging) { yaw -= e.movementX * 0.0022; pitch = Math.max(-1.3, Math.min(1.3, pitch - e.movementY * 0.0022)); } });
  renderer.domElement.addEventListener('mousedown', () => { if (!locked) dragging = true; });
  addEventListener('mouseup', () => dragging = false);
  addEventListener('resize', () => { camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); renderer.setSize(innerWidth, innerHeight); });
  document.getElementById('skip').addEventListener('click', e => { e.stopPropagation(); overlay.style.display = 'none'; overlay.dataset.keep = '1'; });

  const hallOf = z => Math.max(0, Math.min(HALLS.length - 1, Math.floor(-z / L)));
  const clock = new T.Clock(); let lastCard = null;
  function step(dt) {
    const run = keys.ShiftLeft || keys.ShiftRight ? 2 : 1, sp = 6.5 * run;
    const f = (keys.KeyW || keys.ArrowUp ? 1 : 0) - (keys.KeyS || keys.ArrowDown ? 1 : 0), s = (keys.KeyD ? 1 : 0) - (keys.KeyA ? 1 : 0);
    if (keys.ArrowLeft) yaw += 1.8 * dt; if (keys.ArrowRight) yaw -= 1.8 * dt;
    const dir = new T.Vector3(-Math.sin(yaw) * f + Math.cos(yaw) * s, 0, -Math.cos(yaw) * f - Math.sin(yaw) * s);
    if (dir.lengthSq() > 0) dir.normalize().multiplyScalar(sp);
    vel.lerp(dir, Math.min(1, dt * 10));
    const np = pos.clone().addScaledVector(vel, dt);
    // outer bounds
    np.x = Math.max(-W / 2 + 1.2, Math.min(W / 2 - 1.2, np.x)); np.z = Math.max(totalZ + 1.2, Math.min(-0.9, np.z));
    // dividing walls (door gap only)
    for (let i = 1; i < HALLS.length; i++) { const wz = -i * L; if (Math.abs(np.z - wz) < 0.9 && Math.abs(np.x) > DOOR - 0.5) { np.z = pos.z; } }
    for (const c of colliders) { const dx = np.x - c.x, dz = np.z - c.z, d = Math.hypot(dx, dz), r = c.r + 0.4; if (d < r) { np.x = c.x + dx / d * r; np.z = c.z + dz / d * r; } }
    pos.x = np.x; pos.z = np.z; pos.y = 1.75 + Math.sin(performance.now() / 180) * 0.025 * Math.min(1, vel.length() / 5);
    camera.position.copy(pos); camera.rotation.order = 'YXZ'; camera.rotation.set(pitch, yaw, 0);
    // nearest exhibit in view
    const fwd = new T.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw)); let best = null, bs = 0;
    for (const e of exhibits) { const dx = e.x - pos.x, dz = e.z - pos.z, d = Math.hypot(dx, dz); if (d < 10.5) { const dot = (dx * fwd.x + dz * fwd.z) / d, sc = dot * 5 - d / 8; if (dot > 0.82 && sc > bs) { bs = sc; best = e; } } }
    if (best !== lastCard) { lastCard = best; if (best) { const ex = best.ex; card.innerHTML = `<h2>${ex.name}</h2>${ex.years ? `<div class="y">${ex.years}</div>` : ''}<p>${ex.text}</p><h3>On the table</h3><ul>${ex.books.map(b => `<li>${b}</li>`).join('')}</ul>`; card.classList.add('on'); } else card.classList.remove('on'); }
    const hi = hallOf(pos.z); if (hallEl.dataset.h != hi) { hallEl.dataset.h = hi; hallEl.innerHTML = `<b>${HALLS[hi].name}</b><span>${HALLS[hi].sub}</span>`; }
  }
  tp(0); pos.z = -4;
  function loop() { requestAnimationFrame(loop); const dt = Math.min(clock.getDelta(), 0.05), t = clock.elapsedTime; animated.forEach(f => f(t)); step(dt); renderer.render(scene, camera); }
  loop();
})();
