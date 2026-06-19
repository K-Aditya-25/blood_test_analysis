JS = r"""
/* ============================================================
   Vitals — render logic
   ============================================================ */
const DATA = JSON.parse(document.getElementById('data').textContent);
let idx = 0;

const ICON = {organ:'\u{1FA7A}',salt:'\u{1F9C2}',heart:'\u{2764}',cell:'\u{1FA78}',vitamin:'\u{1F48A}',thyroid:'\u{1F98B}',urine:'\u{1F6A7}'};
const M = {normal:'normal',low:'low',high:'high',info:'info',flag:'high'};
const tone = s => M[s] || 'normal';
const valClass = s => 's-' + tone(s);
const STATUS_LABEL = {high:'High',low:'Low',info:'Note',normal:'OK'};

/* display value: prefer text, then numeric, else dash */
function showVal(t){
  if(t.value_text) return t.value_text;
  if(t.value==null || t.value==='') return '\u2014';
  const n = +t.value;
  return (Math.abs(n)>=100 ? n.toFixed(0) : n.toString());
}
function fmtVal(t){
  const v = showVal(t);
  return v;
}
function pct(x,t){ return ((x - t.axis_min)/(t.axis_max - t.axis_min||1))*100; }
function clamp(p){ return Math.max(-2, Math.min(102, p)); }

/* ---- Theme ---- */
const THEME_KEY = 'bta-theme';
function applyTheme(t){
  document.documentElement.setAttribute('data-theme', t);
}
function initTheme(){
  const saved = localStorage.getItem(THEME_KEY);
  const t = saved || (window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  applyTheme(t);
}
function toggleTheme(){
  const cur = document.documentElement.getAttribute('data-theme') || 'light';
  const next = cur==='dark' ? 'light' : 'dark';
  localStorage.setItem(THEME_KEY, next);
  applyTheme(next);
}

/* ---- Wellness ring (SVG) ---- */
function ringEl(pct){
  const r = 54, c = 2*Math.PI*r, off = c * (1 - Math.max(0,Math.min(100,pct))/100);
  return `<svg class="ring" width="130" height="130" viewBox="0 0 130 130">
    <defs><linearGradient id="rg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" style="stop-color:var(--accent-1)"/><stop offset="100%" style="stop-color:var(--accent-2)"/>
    </linearGradient></defs>
    <circle class="track" cx="65" cy="65" r="${r}" stroke-width="12"/>
    <circle class="fill" cx="65" cy="65" r="${r}" stroke-width="12"
      stroke-dasharray="${c.toFixed(1)}" stroke-dashoffset="${off.toFixed(1)}"/>
  </svg><div class="ring-center"><div class="pct">${Math.round(pct)}<span style="font-size:18px">%</span></div>
  <div class="lab">in range</div></div>`;
}

/* ---- Gauge (bullet) ---- */
function gauge(t){
  const v = fmtVal(t);
  const dot = clamp(pct(t.value==null?0:t.value, t));
  let band = '';
  if(t.band_low!=null && t.band_high!=null){
    const l=clamp(pct(t.band_low,t)), w=clamp(pct(t.band_high,t))-l;
    band = `<div class="band" style="left:${l}%;width:${Math.max(w,2)}%"></div>`;
  }
  const ref = t.ref_text || '\u2014';
  const tag = t.status!=='normal' ? `<span class="tag ${tone(t.status)}">${STATUS_LABEL[tone(t.status)]}</span>` : '';
  return `<div class="test"><div class="test-head"><span class="tname">${t.name}${tag}</span>
    <span class="tmeta"><b class="tval ${valClass(t.status)}">${v}${t.unit?` <small>${t.unit}</small>`:''}</b>
    <span class="ref">ref ${ref}</span></span></div>
    <div class="strip">${band}<div class="marker m-${tone(t.status)}" style="left:${dot}%"></div></div>
    <div class="tnote ${t.status!=='normal'?'warn':''}">${t.note||''}</div></div>`;
}

/* ---- Urine tiles ---- */
function urine(tests){
  const ck = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>`;
  return `<div class="grid">`+tests.map(t=>{
    const val = showVal(t);
    const nice = (t.value_text||'').charAt(0).toUpperCase()+t.value_text.slice(1).toLowerCase();
    const label = t.value_text ? nice : val;
    return `<div class="tile"><div class="ck">${ck}</div><div><div class="tn">${t.name}</div><div class="tv">${label}</div></div></div>`;
  }).join('')+`</div>`;
}

/* ---- WBC donut (pure SVG) ---- */
function donut(tests){
  const want=['neutrophils','lymphocytes','monocytes','eosinophils','basophils'];
  const palette=['#3b82f6','#16a34a','#d97706','#7c3aed','#64748b'];
  // theme-aware palette via CSS vars lookup
  const cssVars = getComputedStyle(document.documentElement);
  const colors = ['--info','--normal','--low','--accent-2','--faint'].map(v=>cssVars.getPropertyValue(v).trim()||palette[0]);
  const rows = want.map((k,i)=>{const t=tests.find(x=>x.key===k);return t?{t,c:colors[i]}:null;}).filter(Boolean);
  const R=72, cx=85, cy=85, circ=2*Math.PI*R;
  let acc=0;
  const segs = rows.map(r=>{
    const frac=(r.t.value||0)/100;
    const len=frac*circ, off=acc*circ;
    acc+=frac;
    return {c:r.c, len, off, t:r.t};
  });
  const total = rows.reduce((s,r)=>s+(r.t.value||0),0);
  const arcs = segs.map(s=>`<circle cx="${cx}" cy="${cy}" r="${R}" fill="none"
    stroke="${s.c}" stroke-width="22"
    stroke-dasharray="${s.len.toFixed(2)} ${circ.toFixed(2)}"
    stroke-dashoffset="${(-s.off).toFixed(2)}"
    stroke-linecap="butt"></circle>`).join('');
  return `<div class="donut-wrap">
    <div class="donut-box"><svg width="170" height="170" viewBox="0 0 170 170">${arcs}</svg>
      <div class="donut-center"><div class="n">${Math.round(total)}<span style="font-size:13px">%</span></div>
      <div class="l">WBC diff</div></div></div>
    <ul class="legend">`+rows.map(r=>`<li><span class="sw" style="background:${r.c}"></span>${r.t.name}<b class="pct-v">${r.t.value}%</b></li>`).join('')+`</ul></div>`;
}

/* ---- Priority list (needs attention) ---- */
function priority(p){
  const flagged = p.tests.filter(t=>t.status!=='normal' && t.section!=='urine');
  if(!flagged.length) return '';
  const items = flagged.map(t=>{
    const sec = DATA.sections.find(s=>s.key===t.section);
    return `<a class="prio-item" href="#${t.section}">
      <span class="chip ${tone(t.status)}">${STATUS_LABEL[tone(t.status)][0]}</span>
      <span><div class="pi-n">${t.name}</div>
      <div class="pi-d">${fmtVal(t)}${t.unit?' '+t.unit:''} &middot; <b>${sec?sec.title:t.section}</b></div></span></a>`;
  }).join('');
  return `<div class="priority"><h3>Needs attention <span class="badge">${flagged.length}</span></h3>
    <p class="hint">These results fell outside their healthy range. Tap one to jump to its section.</p>
    <div class="prio-list">${items}</div></div>`;
}

/* ---- Hero ---- */
function hero(p){
  const inRange = p.total_count - p.flagged_count;
  const wpct = p.total_count ? (inRange/p.total_count*100) : 0;
  return `<div class="hero">
    <div class="hero-l">
      <h1>${p.name}</h1>
      <div class="meta"><span>${p.age} yrs</span><span>&middot;</span><span>${p.gender}</span>
        <span>&middot;</span><span>Lab <b>${p.lab_no}</b></span><span>&middot;</span><span>Collected <b>${p.collected}</b></span></div>
      <div class="headline">${p.headline}</div>
      <div class="hero-pills">
        <span class="pill ok"><span class="pd"></span>${inRange} in range</span>
        <span class="pill flag"><span class="pd"></span>${p.flagged_count} to review</span>
        <span class="pill ok" style="background:var(--info-soft);color:var(--info);border-color:color-mix(in srgb,var(--info) 24%,transparent)"><span class="pd" style="background:var(--info)"></span>${p.total_count} tests</span>
      </div>
    </div>
    <div class="ring-wrap">${ringEl(wpct)}</div>
  </div>`;
}

/* ---- Section card ---- */
function sectionCard(s,p){
  const tests = p.tests.filter(t=>t.section===s.key);
  if(!tests.length) return '';
  const diff=['neutrophils','lymphocytes','monocytes','eosinophils','basophils'];
  let body;
  if(s.key==='urine') body=urine(tests);
  else if(s.key==='blood_cells') body=donut(tests)+tests.filter(t=>!diff.includes(t.key)).map(gauge).join('');
  else body=tests.map(gauge).join('');
  const summ = p.section_summary[s.key] || '';
  return `<section class="card" id="${s.key}">
    <div class="card-h"><div class="card-ic">${ICON[s.icon]||'\u{1F4CA}'}</div>
      <div><h2>${s.title}</h2><div class="area">${s.area||''}</div></div></div>
    <p class="story">${s.story}</p>
    ${summ?`<div class="secsum">${summ}</div>`:''}${body}</section>`;
}

/* ---- Section nav ---- */
function secnav(){
  return `<nav class="secnav">`+DATA.sections.map(s=>{
    const cnt = DATA.patients[idx].tests.filter(t=>t.section===s.key).length;
    return `<a href="#${s.key}" data-sec="${s.key}">${s.title}<span style="opacity:.6;margin-left:5px">${cnt}</span></a>`;
  }).join('')+`</nav>`;
}

/* ---- Render ---- */
function render(){
  const p = DATA.patients[idx];
  let h = hero(p) + priority(p) + secnav();
  for(const s of DATA.sections) h += sectionCard(s,p);
  const app = document.getElementById('app');
  app.innerHTML = h;
  app.classList.remove('in'); void app.offsetWidth; app.classList.add('in');
  initSecnav();
  window.scrollTo({top:0,behavior:'smooth'});
}

/* active section nav on scroll */
function initSecnav(){
  const links = [...document.querySelectorAll('.secnav a')];
  const map = {};
  links.forEach(a=>{ const el=document.getElementById(a.dataset.sec); if(el) map[a.dataset.sec]=el; });
  if(!links.length) return;
  const obs = new IntersectionObserver((ents)=>{
    ents.forEach(e=>{
      if(e.isIntersecting) links.forEach(a=>a.classList.toggle('active', a.dataset.sec===e.target.id));
    });
  },{rootMargin:'-90px 0px -65% 0px',threshold:0});
  Object.values(map).forEach(el=>obs.observe(el));
  links[0] && links[0].classList.add('active');
}

/* ---- wire up ---- */
function initSwitcher(){
  const box = document.getElementById('switcher');
  if(!box) return;
  DATA.patients.forEach((p,i)=>{
    const b = document.createElement('button');
    b.dataset.i = i;
    b.dataset.flag = p.flagged_count? '1':'0';
    b.innerHTML = `<span class="dot"></span><span>${p.first_name}</span>`;
    b.onclick = ()=>{ if(idx!==i){ idx=i; render(); syncSwitcher(); } };
    box.appendChild(b);
  });
  syncSwitcher();
}
function syncSwitcher(){
  [...document.querySelectorAll('#switcher button')].forEach(b=>{
    b.classList.toggle('active', +b.dataset.i===idx);
  });
}

initTheme();
document.querySelector('.theme-toggle').addEventListener('click', toggleTheme);
initSwitcher();
render();
"""
