/* PopBook: a paper pop-up book on a desk, with a step-by-step text panel. Shared by the IELTS pop-up lessons. */
var PopBook=(function(){
  function $(s,r){return (r||document).querySelector(s)}
  function $$(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))}
  var C={INK:'#22304a',CREAM:'#f3e7cf',CORAL:'#e2573d',MUST:'#e9b44c',TEAL:'#2f8f83',SKY:'#9ccbe0',WOOD:'#b9773f',WOOD2:'#8f5a2e',NAVY:'#2b3d5e',GREEN:'#6fa86a',WHITE:'#fbf6ea',PEACH:'#f0c3a0',BLUE:'#2b5d8f',RED2:'#b9432d',GREEN2:'#4f8a55',STONE:'#b9b3a6'};
  var P={S:{keep:{}},C:C,PY:.42,onClick:null,hoverText:null,onTimer:null,$:$,$$:$$};
  var ok=false,ren,scene,cam,canvas,wrap,ray,hits=[],pops=[],sprites=[],ticks=[],tgt,th=0,ph=1,rad=30,tw=null,FOV=42,vert=5;
  var T=.03,L=.045,B=.05,grain,mats={},edgeMat,ghost;
  function lin(h){return new THREE.Color(h).convertSRGBToLinear()}
  function mk(w,h){var cv=document.createElement('canvas');cv.width=w;cv.height=h;return cv}
  function tex(cv){var t=new THREE.CanvasTexture(cv);t.encoding=THREE.sRGBEncoding;t.anisotropy=8;return t}
  function paperMat(col){if(!mats[col])mats[col]=new THREE.MeshStandardMaterial({color:lin(col),map:grain,bumpMap:grain,bumpScale:.01,roughness:.93,metalness:0});return mats[col]}
  function rrShape(w,h,r){var s=new THREE.Shape(),x=-w/2,y=0;r=Math.min(r,w/2,h/2);
    s.moveTo(x+r,y);s.lineTo(x+w-r,y);s.quadraticCurveTo(x+w,y,x+w,y+r);s.lineTo(x+w,y+h-r);s.quadraticCurveTo(x+w,y+h,x+w-r,y+h);
    s.lineTo(x+r,y+h);s.quadraticCurveTo(x,y+h,x,y+h-r);s.lineTo(x,y+r);s.quadraticCurveTo(x,y,x+r,y);return s}
  function polyShape(pts){var s=new THREE.Shape();pts.forEach(function(p,i){i?s.lineTo(p[0],p[1]):s.moveTo(p[0],p[1])});return s}
  function circShape(r){var s=new THREE.Shape();s.absarc(0,0,r,0,Math.PI*2,false);return s}
  function cut(g,shape,col,x,y,layer){var m=new THREE.Mesh(new THREE.ExtrudeGeometry(shape,{depth:T,bevelEnabled:false,curveSegments:10}),[typeof col==='string'?paperMat(col):col,edgeMat]);
    m.position.set(x,y,layer*L);m.castShadow=m.receiveShadow=true;g.add(m);return m}
  function rr(g,x,y,w,h,r,col,layer,border){if(border)cut(g,rrShape(w+2*B,h+2*B,r+B),C.WHITE,x,y-B,layer-.5);return cut(g,rrShape(w,h,r),col,x,y,layer)}
  function poly(g,pts,col,layer){return cut(g,polyShape(pts),col,0,0,layer)}
  function circ(g,x,y,r,col,layer,border){if(border)cut(g,circShape(r+B),C.WHITE,x,y,layer-.5);return cut(g,circShape(r),col,x,y,layer)}
  /* a piece lying flat on the page; shape's y runs away from you */
  function flat(shape,col,x,z,lift){var o=new THREE.Mesh(new THREE.ExtrudeGeometry(shape,{depth:T,bevelEnabled:false,curveSegments:10}),typeof col==='string'?paperMat(col):col);o.rotation.x=-Math.PI/2;o.position.set(x,P.PY+(lift||0),z);o.receiveShadow=true;o.castShadow=true;scene.add(o);return o}
  function solid(w,h,d,col,x,y,z,rough){var m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),new THREE.MeshStandardMaterial({color:lin(col),roughness:rough||.8}));m.position.set(x,y,z);m.castShadow=m.receiveShadow=true;scene.add(m);return m}
  function words(g,w,h,x,y,layer,draw){var cv=mk(Math.round(w*200),Math.round(h*200));draw(cv.getContext('2d'),cv.width,cv.height);
    var m=new THREE.Mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshStandardMaterial({map:tex(cv),transparent:true,roughness:.95,alphaTest:.02}));
    m.position.set(x,y+h/2,layer*L+T+.004);g.add(m);m.userData.cv=cv;return m}
  /* a white paper sign with a title and a small line under it */
  function sign(g,x,y,w,h,title,sub,col,layer){layer=layer||0;rr(g,x,y,w,h,.08,C.WHITE,layer,false);
    return words(g,w,h,x,y,layer,function(c,W,H){c.textAlign='center';c.textBaseline='middle';c.fillStyle=C.INK;var s=H*(sub?.46:.56);c.font='400 '+s+'px "Abril Fatface", Georgia, serif';
      while(c.measureText(title).width>W*.9&&s>10){s-=2;c.font='400 '+s+'px "Abril Fatface", Georgia, serif'}c.fillText(title,W/2,H*(sub?.38:.52));
      if(sub){c.fillStyle=col||C.CORAL;var f=H*.2;c.font='700 '+f+'px "DM Sans", sans-serif';var t=sub.toUpperCase().split('').join(' ');while(c.measureText(t).width>W*.92&&f>8){f-=1;c.font='700 '+f+'px "DM Sans", sans-serif'}c.fillText(t,W/2,H*.78)}})}
  function popup(x,z,rotY,parent){var outer=new THREE.Group();outer.position.set(x,P.PY,z);outer.rotation.y=rotY||0;(parent||scene).add(outer);
    var g=new THREE.Group();g.rotation.x=-Math.PI/2;g.visible=false;outer.add(g);var p={g:g,outer:outer,open:false,p:0,t0:0,from:0,lean:0,wob:0};pops.push(p);return p}
  function fold(p,open,delay){if(p.open===open&&(open?p.p>0:p.p===0))return;p.open=open;p.from=p.p;p.t0=performance.now()+(delay||0)}
  function back(k){var c=1.9;return 1+(c+1)*Math.pow(k-1,3)+c*Math.pow(k-1,2)}
  function drawLabel(cv,text,bg,fg){var x=cv.getContext('2d');x.clearRect(0,0,cv.width,cv.height);if(!text)return;
    var r=22,w=cv.width-8,h=cv.height-8;x.fillStyle=bg;x.beginPath();x.moveTo(4+r,4);x.arcTo(4+w,4,4+w,4+h,r);x.arcTo(4+w,4+h,4,4+h,r);x.arcTo(4,4+h,4,4,r);x.arcTo(4,4,4+w,4,r);x.fill();
    var f='px "DM Sans", "Segoe UI", Arial, sans-serif',size=56;x.font='700 '+size+f;while(x.measureText(text).width>w-36&&size>20){size-=2;x.font='700 '+size+f}
    x.fillStyle=fg;x.textAlign='center';x.textBaseline='middle';x.fillText(text,cv.width/2,cv.height/2+2)}
  function label(text,bg,fg,width){var cv=mk(512,128);drawLabel(cv,text,bg,fg);var t=new THREE.CanvasTexture(cv);t.minFilter=THREE.LinearFilter;t.encoding=THREE.sRGBEncoding;
    var s=new THREE.Sprite(new THREE.SpriteMaterial({map:t,transparent:true,depthTest:false,toneMapped:false}));s.scale.set(width,width/4,1);s.renderOrder=10;s.userData={cv:cv,tex:t};scene.add(s);return s}
  function relabel(sp,text,bg,fg){drawLabel(sp.userData.cv,text,bg,fg);sp.userData.tex.needsUpdate=true}
  function hit(w,h,d,x,y,z,data){var m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),ghost);m.position.set(x,y,z);m.userData.hit=data;scene.add(m);hits.push(m);return m}
  function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
  function fit(width,v){var a=cam.aspect,t=Math.tan(FOV*Math.PI/360);return Math.max((width/2)/(t*a),(v||vert)/t*.95)}
  function view(to,instant){if(!ok)return;to={x:to.x||0,y:to.y===undefined?1.2:to.y,z:to.z||0,th:to.th||0,ph:to.ph||1.02,r:fit(to.w||20,to.v)*(to.k||1.06)};
    if(instant){tgt.set(to.x,to.y,to.z);th=to.th;ph=to.ph;rad=to.r;tw=null;return}
    tw={t0:performance.now(),from:{x:tgt.x,y:tgt.y,z:tgt.z,th:th,ph:ph,r:rad},to:to}}
  function ease(k){return k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2}
  /* a little paper traveller who can walk and hop about the page */
  function walker(x,z){var o=new THREE.Group();o.position.set(x,P.PY,z);scene.add(o);var g=new THREE.Group();g.rotation.x=-.05;o.add(g);
    rr(g,-.13,0,.14,.42,.04,C.INK,0,true);rr(g,.13,0,.14,.42,.04,C.INK,0,true);rr(g,0,.34,.62,.68,.2,C.CORAL,1,true);
    rr(g,0,.84,.5,.14,.06,C.MUST,2);var sc=rr(g,.2,.6,.13,.32,.05,C.MUST,2);sc.rotation.z=-.25;circ(g,0,1.2,.25,C.PEACH,1.5,true);
    poly(g,[[-.26,1.25],[-.2,1.5],[.2,1.5],[.26,1.25],[.1,1.36],[-.1,1.36]],C.INK,2.5);
    var W={o:o,q:[],go:function(x,z,y,ms,hop){W.q.push({x:x,z:z,y:(y||0)+P.PY,ms:ms||500,hop:hop===undefined?.5:hop});return W},
      jump:function(x,z,y){W.q=[];W.cur=null;o.position.set(x,(y||0)+P.PY,z);return W},stop:function(){W.q=[];W.cur=null}};
    ticks.push(function(now){if(!W.cur&&W.q.length){var n=W.q.shift();W.cur={t0:now,f:o.position.clone(),n:n}}
      if(W.cur){var c=W.cur,k=Math.min(1,(now-c.t0)/c.n.ms),e=ease(k);o.position.set(c.f.x+(c.n.x-c.f.x)*e,c.f.y+(c.n.y-c.f.y)*e+Math.sin(k*Math.PI)*c.n.hop,c.f.z+(c.n.z-c.f.z)*e);
        g.rotation.z=Math.sin(k*Math.PI*4)*.07*(c.n.ms>900?1:0);if(k>=1){W.cur=null;g.rotation.z=0}}});
    return W}

  function init3d(o){
    canvas=$('#house');wrap=$('#houseWrap');
    try{ren=new THREE.WebGLRenderer({canvas:canvas,antialias:true})}catch(e){ren=null}
    if(!ren){$('#nogl').style.display='flex';canvas.style.display='none';return}
    ren.setPixelRatio(Math.min(window.devicePixelRatio||1,2));ren.setClearColor(0x140d08);
    ren.outputEncoding=THREE.sRGBEncoding;ren.toneMapping=THREE.ACESFilmicToneMapping;ren.toneMappingExposure=.98;
    ren.shadowMap.enabled=true;ren.shadowMap.type=THREE.PCFSoftShadowMap;
    scene=new THREE.Scene();scene.fog=new THREE.Fog(0x140d08,60,150);cam=new THREE.PerspectiveCamera(FOV,1,.1,300);
    scene.add(new THREE.HemisphereLight(0xd6defc,0x4a2f1c,.5));
    var lamp=new THREE.SpotLight(0xffdfb0,1.85,110,.74,.65,1.1);lamp.position.set(-11,24,15);lamp.target.position.set(0,0,-.5);
    lamp.castShadow=true;lamp.shadow.mapSize.set(2048,2048);lamp.shadow.bias=-.0007;lamp.shadow.radius=4;lamp.shadow.camera.near=8;lamp.shadow.camera.far=70;scene.add(lamp,lamp.target);
    var fill=new THREE.DirectionalLight(0x9fb6ff,.2);fill.position.set(12,8,6);scene.add(fill);
    ray=new THREE.Raycaster();ghost=new THREE.MeshBasicMaterial({transparent:true,opacity:0,depthWrite:false});tgt=new THREE.Vector3(0,1,.6);
    edgeMat=new THREE.MeshStandardMaterial({color:lin('#fffaf0'),roughness:.95});
    grain=(function(){var cv=mk(256,256),x=cv.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,256,256);
      var d=x.getImageData(0,0,256,256),p=d.data;for(var i=0;i<p.length;i+=4){var n=232+Math.random()*23|0;p[i]=p[i+1]=p[i+2]=n}x.putImageData(d,0,0);
      var t=tex(cv);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(.55,.55);return t})();
    P.scene=scene;P.THREE=THREE;
    /* desk */
    (function(){var cv=mk(1024,1024),x=cv.getContext('2d');var g=x.createLinearGradient(0,0,1024,0);g.addColorStop(0,'#6a3f22');g.addColorStop(.5,'#7b4a28');g.addColorStop(1,'#633a1f');x.fillStyle=g;x.fillRect(0,0,1024,1024);
      for(var i=0;i<900;i++){x.globalAlpha=.04+Math.random()*.08;x.strokeStyle=Math.random()<.5?'#2e1a0c':'#a8703f';x.lineWidth=.6+Math.random()*2;var y=Math.random()*1024;
        x.beginPath();x.moveTo(0,y);for(var k=1;k<=8;k++)x.lineTo(k*128,y+Math.sin(k*1.3+i)*6);x.stroke()}
      x.globalAlpha=.35;x.strokeStyle='#2a170a';x.lineWidth=3;[256,512,768].forEach(function(y){x.beginPath();x.moveTo(0,y);x.lineTo(1024,y);x.stroke()});
      var t=tex(cv);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(5,5);
      var m=new THREE.Mesh(new THREE.PlaneGeometry(260,260),new THREE.MeshStandardMaterial({map:t,roughness:.55,metalness:.05}));m.rotation.x=-Math.PI/2;m.receiveShadow=true;scene.add(m)})();
    /* book */
    var bk=o.book,PW=bk.w,PD=bk.d,PZ=bk.z||0;vert=PD/2+1.4;P.book={w:PW,d:PD,z:PZ};
    solid(PW+.8,.14,PD+.8,bk.cover||'#1f2c47',0,.07,PZ,.6);solid(PW,.26,PD,'#e9dcc0',0,.27,PZ,.95);
    (function(){var k=80,cv=mk(Math.round(PW*k),Math.round(PD*k)),x=cv.getContext('2d'),W=cv.width,H=cv.height;x.fillStyle='#e6d6b2';x.fillRect(0,0,W,H);
      x.globalAlpha=.7;x.fillStyle='#d6c298';for(var i=0;i*70<W;i++)for(var j=0;j*70<H;j++){var px=30+i*70+(j%2)*35,py=30+j*70;x.fillRect(px-6,py-1.5,12,3);x.fillRect(px-1.5,py-6,3,12)}
      x.globalAlpha=1;
      var X=function(v){return (v+PW/2)*k},Z=function(v){return (v-PZ+PD/2)*k};
      (bk.folds||[]).forEach(function(f){var gx=X(f),g=x.createLinearGradient(gx-70,0,gx+70,0);g.addColorStop(0,'rgba(60,40,20,0)');g.addColorStop(.5,'rgba(60,40,20,.3)');g.addColorStop(1,'rgba(60,40,20,0)');x.fillStyle=g;x.fillRect(gx-70,0,140,H)});
      if(o.page)o.page(x,k,X,Z,W,H);
      x.fillStyle=C.INK;x.font='700 24px "DM Sans", sans-serif';x.textBaseline='middle';x.textAlign='left';x.fillText((bk.left||'').toUpperCase().split('').join(' '),50,H-36);
      x.textAlign='right';x.fillText((bk.right||'').toUpperCase().split('').join(' '),W-50,H-36);
      var m=new THREE.Mesh(new THREE.PlaneGeometry(PW,PD),new THREE.MeshStandardMaterial({map:tex(cv),bumpMap:grain,bumpScale:.006,roughness:.95}));
      m.rotation.x=-Math.PI/2;m.position.set(0,P.PY-.012,PZ);m.receiveShadow=true;scene.add(m)})();
    var down=null;
    function pick(e){var r=canvas.getBoundingClientRect(),v=new THREE.Vector2(((e.clientX-r.left)/r.width)*2-1,-((e.clientY-r.top)/r.height)*2+1);
      ray.setFromCamera(v,cam);var h=ray.intersectObjects(hits,false);for(var i=0;i<h.length;i++)if(h[i].object.visible&&!h[i].object.userData.off)return h[i].object.userData.hit;return null}
    canvas.addEventListener('pointerdown',function(e){down={x:e.clientX,y:e.clientY,th:th,ph:ph,moved:false};canvas.setPointerCapture&&canvas.setPointerCapture(e.pointerId);canvas.style.cursor='grabbing'});
    canvas.addEventListener('pointermove',function(e){
      if(down){var dx=e.clientX-down.x,dy=e.clientY-down.y;if(Math.abs(dx)+Math.abs(dy)>6)down.moved=true;
        if(down.moved){tw=null;th=clamp(down.th-dx*.006,-1.15,1.15);ph=clamp(down.ph-dy*.005,.3,1.45)}}
      else{var u=pick(e),el=$('#hover'),t=u&&P.hoverText?P.hoverText(u):null;if(t){el.textContent=t;el.style.display='block';canvas.style.cursor='pointer'}else{el.style.display='none';canvas.style.cursor='grab'}}});
    canvas.addEventListener('pointerup',function(e){canvas.style.cursor='grab';if(down&&!down.moved){var u=pick(e);if(u&&P.onClick)P.onClick(u)}down=null});
    canvas.addEventListener('pointercancel',function(){down=null});
    canvas.addEventListener('pointerleave',function(){$('#hover').style.display='none'});
    canvas.addEventListener('wheel',function(e){e.preventDefault();tw=null;rad=clamp(rad*(e.deltaY>0?1.08:.93),5,80)},{passive:false});
    $('#zin').addEventListener('click',function(){tw=null;rad=clamp(rad*.82,5,80)});
    $('#zout').addEventListener('click',function(){tw=null;rad=clamp(rad*1.22,5,80)});
    if(window.ResizeObserver)new ResizeObserver(resize).observe(wrap);
    window.addEventListener('resize',resize);
    ok=true;resize();o.build(P);requestAnimationFrame(frame);
  }
  function resize(){if(!ok)return;var w=wrap.clientWidth,h=wrap.clientHeight;if(!w||!h)return;ren.setSize(w,h,false);cam.aspect=w/h;cam.updateProjectionMatrix();ren.render(scene,cam)}
  function frame(now){requestAnimationFrame(frame);
    if(tw){var k=Math.min(1,(now-tw.t0)/900),e=ease(k),f=tw.from,t=tw.to;
      tgt.set(f.x+(t.x-f.x)*e,f.y+(t.y-f.y)*e,f.z+(t.z-f.z)*e);th=f.th+(t.th-f.th)*e;ph=f.ph+(t.ph-f.ph)*e;rad=f.r+(t.r-f.r)*e;if(k>=1)tw=null}
    pops.forEach(function(p){if(!p.open&&p.p===0&&now>p.t0){p.g.visible=false;return}var k=clamp((now-p.t0)/(p.open?700:300),0,1),to=p.open?1:0;
      p.p=now<p.t0?p.from:(p.open?p.from+(to-p.from)*back(k):p.from+(to-p.from)*k*k);var wob=0;if(p.wob){var a=(now-p.wob)/600;if(a<1)wob=Math.sin(a*Math.PI*3)*.16*(1-a);else p.wob=0}
      p.g.rotation.x=-Math.PI/2+(Math.PI/2+p.lean)*p.p+wob+Math.sin(now/1700+p.outer.position.x)*.006*p.p;p.g.visible=p.p>.004});
    for(var i=0;i<ticks.length;i++)ticks[i](now);
    var sway=tw?0:Math.sin(now/5200)*.03;
    cam.position.set(tgt.x+rad*Math.sin(ph)*Math.sin(th+sway),tgt.y+rad*Math.cos(ph),tgt.z+rad*Math.sin(ph)*Math.cos(th+sway));cam.lookAt(tgt);
    ren.render(scene,cam)}
  P.lin=lin;P.rr=rr;P.poly=poly;P.circ=circ;P.cut=cut;P.flat=flat;P.solid=solid;P.words=words;P.sign=sign;P.popup=popup;P.fold=fold;P.label=label;P.relabel=relabel;P.hit=hit;P.view=view;
  P.rrShape=rrShape;P.polyShape=polyShape;P.circShape=circShape;P.paperMat=paperMat;P.walker=walker;P.tick=function(f){ticks.push(f)};P.wob=function(p){p.wob=performance.now()};

  /* ---------------- the text panel ---------------- */
  var steps=[],stages=[],cur=-1,timers={};
  function say(id,kind,msg){var f=$('#'+id);if(f){f.className='fb '+kind;f.innerHTML=msg}}
  P.say=say;
  function fmt(s){return Math.floor(s/60)+':'+('0'+s%60).slice(-2)}
  function stopTimers(){Object.keys(timers).forEach(function(k){clearInterval(timers[k].iv)});timers={}}
  function startTimer(btn){var id=btn.getAttribute('data-timer'),sec=+btn.getAttribute('data-sec'),el=$('#'+id);
    if(timers[id]){clearInterval(timers[id].iv);delete timers[id];btn.textContent=btn.getAttribute('data-label');if(el){el.textContent=fmt(sec);el.className='clock'}if(P.onTimer)P.onTimer(id,-1,sec);return}
    if(!btn.getAttribute('data-label'))btn.setAttribute('data-label',btn.textContent);btn.textContent='Stop';var left=sec;if(el){el.textContent=fmt(left);el.className='clock'}
    if(P.onTimer)P.onTimer(id,sec,sec);
    timers[id]={iv:setInterval(function(){left--;if(el){el.textContent=fmt(Math.max(0,left));el.className='clock'+(left<=0?' red':left<=sec*.2?' warn':'')}
      if(P.onTimer)P.onTimer(id,left,sec);if(left<=0){clearInterval(timers[id].iv);delete timers[id];btn.textContent=btn.getAttribute('data-label')}},1000)}}
  function restore(){$$('[data-keep]').forEach(function(el){var v=P.S.keep[el.getAttribute('data-keep')];if(v===undefined)return;if(el.type==='checkbox')el.checked=!!v;else el.value=v});$$('textarea[data-count]').forEach(count)}
  function count(el){var w=el.value.trim()?el.value.trim().split(/\s+/).length:0,o=$('#'+el.getAttribute('data-count'));if(o)o.textContent=w+' word'+(w===1?'':'s')}
  function show(i){if(i<0||i>=steps.length)return;if(cur>=0&&steps[cur].leave)steps[cur].leave(P);stopTimers();P.onClick=null;P.hoverText=null;P.onTimer=null;cur=i;var s=steps[i];
    $('#pbody').innerHTML=typeof s.html==='function'?s.html(P):s.html;$('#pbody').scrollTop=0;restore();
    $('#pcount').textContent=(i+1)+' / '+steps.length;$('#back').disabled=i===0;$('#next').disabled=i===steps.length-1;
    $$('.stg').forEach(function(b,k){b.classList.toggle('active',k===s.stage)});
    if(s.enter&&ok)s.enter(P);resize()}
  P.show=show;P.redraw=function(){show(cur)};
  function barSpace(){var h=0;$$('body > *').forEach(function(el){if(el.id==='app'||el.id==='sheet')return;var cs=getComputedStyle(el);
    if(cs.position==='fixed'&&cs.display!=='none'){var r=el.getBoundingClientRect();if(r.height<220&&r.bottom>=innerHeight-2)h=Math.max(h,r.height)}});
    document.documentElement.style.setProperty('--bar',h+'px')}
  function run(o){stages=o.stages;steps=o.steps;
    var nav=$('#stages');stages.forEach(function(n,k){var b=document.createElement('button');b.className='stg';b.textContent=n;b.addEventListener('click',function(){for(var i=0;i<steps.length;i++)if(steps[i].stage===k){show(i);break}});nav.appendChild(b)});
    var vb=$('#views');(o.views||[]).forEach(function(v){var b=document.createElement('button');b.className='chip';b.textContent=v.name;b.addEventListener('click',function(){view(v.v)});vb.appendChild(b)});
    $('#back').addEventListener('click',function(){show(cur-1)});$('#next').addEventListener('click',function(){show(cur+1)});
    $('#hide').addEventListener('click',function(){var p=$('#panel');p.classList.toggle('shut');this.textContent=p.classList.contains('shut')?'Show text':'Hide text';resize()});
    document.addEventListener('click',function(e){var t=e.target.closest('[data-reveal],[data-sheet],[data-close],[data-timer],[data-a]');if(!t)return;
      if(t.hasAttribute('data-reveal')){var r=$('#'+t.getAttribute('data-reveal'));if(r)r.classList.toggle('show')}
      else if(t.hasAttribute('data-sheet')){$$('.sh').forEach(function(s){s.classList.toggle('on',s.id===t.getAttribute('data-sheet'))});$('#sheet').classList.add('open')}
      else if(t.hasAttribute('data-close'))$('#sheet').classList.remove('open')
      else if(t.hasAttribute('data-timer'))startTimer(t)
      else if(steps[cur]&&steps[cur].act)steps[cur].act(t.getAttribute('data-a'),t,P)});
    $('#sheet').addEventListener('click',function(e){if(e.target===this)this.classList.remove('open')});
    document.addEventListener('input',function(e){var el=e.target;if(el.hasAttribute&&el.hasAttribute('data-keep'))P.S.keep[el.getAttribute('data-keep')]=el.type==='checkbox'?el.checked:el.value;if(el.hasAttribute&&el.hasAttribute('data-count'))count(el)});
    function go(){if(run.done)return;run.done=true;init3d(o);if(o.home)view(o.home,true);show(0);barSpace();setInterval(barSpace,1500)}
    if(document.fonts&&document.fonts.load){Promise.all([document.fonts.load('40px "Abril Fatface"'),document.fonts.load('700 20px "DM Sans"')]).then(go,go);setTimeout(go,1800)}else go()}
  return{run:run,P:P};
})();
