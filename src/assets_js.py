JS = r"""
const DATA = JSON.parse(document.getElementById('data').textContent);
let idx = 0, chart = null;
const ICON = {organ:'🩺',salt:'🧂',heart:'❤️',cell:'🩸',vitamin:'💊',thyroid:'🦋',urine:'🚰'};
const M = {normal:'normal',low:'low',high:'high',info:'info',flag:'high'};
const tone = s => M[s] || 'normal';
const valClass = s => 's-' + tone(s);

function pct(x, t){ return ((x - t.axis_min)/(t.axis_max - t.axis_min||1))*100; }

function bullet(t){
  const v = t.value_text || (t.value==null?'':t.value);
  const dot = pct(t.value==null?0:t.value, t);
  let band = '';
  if(t.band_low!=null && t.band_high!=null){
    const l=pct(t.band_low,t), w=pct(t.band_high,t)-l;
    band = `<div class="band" style="left:${l}%;width:${w}%"></div>`;
  }
  const ref = t.ref_text || '';
  return `<div class="test"><div class="test-head"><span class="tname">${t.name}</span>
    <span class="tmeta"><b class="tval ${valClass(t.status)}">${v} <small>${t.unit}</small></b>
    <span class="ref">${ref||'—'}</span></span></div>
    <div class="strip">${band}<div class="marker m-${tone(t.status)}" style="left:${dot}%"></div></div>
    <div class="tnote">${t.note}</div></div>`;
}

function urine(tests){
  return `<div class="grid">`+tests.map(t=>`<div class="tile ok"><div class="tn">${t.name}</div>
    <div class="tv">${t.value_text||'—'}</div></div>`).join('')+`</div>`;
}

function donut(tests){
  const want=['neutrophils','lymphocytes','monocytes','eosinophils','basophils'];
  const colors=['#2563eb','#16a34a','#d97706','#7c3aed','#64748b'];
  const rows=want.map((k,i)=>{const t=tests.find(x=>x.key===k);return t?{t,c:colors[i]}:null;}).filter(Boolean);
  const html=`<div class="donut-wrap"><canvas id="wbc" width="180" height="180"></canvas>
    <ul class="legend">`+rows.map(r=>`<li><span style="color:${r.c}">●</span> ${r.t.name}: <b>${r.t.value}%</b></li>`).join('')+`</ul></div>`;
  setTimeout(()=>initDonut(rows),0);
  return html;
}

function initDonut(rows){
  const el=document.getElementById('wbc'); if(!el)return;
  chart=new Chart(el,{type:'doughnut',data:{labels:rows.map(r=>r.t.name),
    datasets:[{data:rows.map(r=>r.t.value),backgroundColor:rows.map(r=>r.c),borderColor:'#fff',borderWidth:2}]},
    options:{cutout:'62%',plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>` ${c.label}: ${c.raw}%`}}}}});
}

function render(){
  if(chart){chart.destroy();chart=null;}
  const p=DATA.patients[idx], next=DATA.patients[1-idx];
  document.getElementById('next-name').textContent = next.first_name;
  let h=`<div class="hero"><h1>${p.name}</h1>
    <div class="meta">${p.age} yrs · ${p.gender} · Lab ${p.lab_no} · Collected ${p.collected}</div>
    <div class="headline">${p.headline}</div>
    <div style="margin-top:12px"><span class="pill ok">${p.total_count-p.flagged_count} in range</span>
    <span class="pill flag">${p.flagged_count} to review</span></div></div>`;
  const diff=['neutrophils','lymphocytes','monocytes','eosinophils','basophils'];
  for(const s of DATA.sections){
    const tests=p.tests.filter(t=>t.section===s.key);
    if(!tests.length)continue;
    let body;
    if(s.key==='urine') body=urine(tests);
    else if(s.key==='blood_cells') body=donut(tests)+tests.filter(t=>!diff.includes(t.key)).map(bullet).join('');
    else body=tests.map(bullet).join('');
    const summ=p.section_summary[s.key]||'';
    h+=`<div class="card"><h2>${ICON[s.icon]||'📊'} ${s.title}</h2>
      <p class="story">${s.story}</p>${summ?`<div class="secsum">${summ}</div>`:''}${body}</div>`;
  }
  document.getElementById('app').innerHTML=h;
}
document.getElementById('toggle').onclick=()=>{idx=1-idx;render();};
render();
"""
