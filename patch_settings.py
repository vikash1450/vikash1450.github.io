CSS=r'''html[data-theme="light"]{--bg:#fff;--fg:#1b1b1b;--mute:#6c6c6c;--card:#f1f1f1;--line:#e3e3e3;--pill:#e6efff;--pillfg:#1558d6}
html[data-theme="dark"]{--bg:#141414;--fg:#ececec;--mute:#9b9b9b;--card:#2a2a2a;--line:#343434;--pill:#1c2a47;--pillfg:#8ab4ff}
#sets{position:fixed;inset:0;z-index:60;background:var(--bg);color:var(--fg);overflow-y:auto;padding:calc(12px + env(safe-area-inset-top,0px)) 16px 40px}
#sets[hidden]{display:none}
#sback{background:var(--card);border:0;border-radius:50%;width:40px;height:40px;font-size:20px;color:var(--fg);cursor:pointer}
.sav{width:76px;height:76px;border-radius:50%;background:var(--blue);color:#fff;font-size:30px;display:flex;align-items:center;justify-content:center;margin:0 auto 8px}
.snm{text-align:center;font-weight:600;margin-bottom:16px}
.sh{color:var(--mute);font-size:14px;margin:18px 6px 8px}
.sg{background:var(--card);border-radius:20px;overflow:hidden}
.si{display:flex;align-items:center;gap:14px;padding:15px 16px;border-bottom:1px solid var(--bg);cursor:pointer}
.si:last-child{border-bottom:0}
.si .ic{font-size:20px;width:26px;text-align:center}
.si .tx{display:flex;flex-direction:column}
.si .tx i{font-style:normal;color:var(--mute);font-size:13px}
.slo .tx b{color:#e5484d}
.ssel{margin-left:auto;background:var(--bg);color:var(--fg);border:1px solid var(--line);border-radius:10px;padding:6px}
.sdots{margin-left:auto;display:flex;gap:8px}
.sdot{width:26px;height:26px;border-radius:50%;border:2px solid var(--bg);cursor:pointer}
#toast{position:fixed;left:50%;bottom:90px;transform:translateX(-50%);background:#222;color:#fff;padding:10px 16px;border-radius:20px;z-index:80;font-size:14px}
#toast[hidden]{display:none}
#about #setbtn{width:100%;padding:10px;margin-bottom:8px;border:0;border-radius:12px;background:var(--card);color:var(--fg);font:inherit;cursor:pointer}'''
HTML=r'''<div id="sets" hidden><button id="sback" aria-label="Wapas">&larr;</button><div id="sbody"></div></div>
<div id="toast" hidden></div>
'''
JS=r'''(function(){
const LS=(k,v)=>{try{if(v===undefined)return localStorage.getItem(k);v===null?localStorage.removeItem(k):localStorage.setItem(k,v)}catch(e){return null}};
const COL={Blue:'#2f6bff',Green:'#1aa260',Purple:'#7b4dff',Orange:'#f07a1a',Pink:'#e0407a'};
function applyTheme(){const t=LS('oai_theme')||'system';const r=document.documentElement;if(t==='system')r.removeAttribute('data-theme');else r.setAttribute('data-theme',t);r.style.setProperty('--blue',COL[LS('oai_accent')||'Blue']||COL.Blue)}
applyTheme();
let tm;function toast(m){const e=document.getElementById('toast');e.textContent=m;e.hidden=false;clearTimeout(tm);tm=setTimeout(()=>{e.hidden=true},2200)}
const soon=()=>toast('Jald aa raha hai \u{1F6A7}');
function row(ic,label,sub,fn){const b=document.createElement('div');b.className='si';b.innerHTML='<span class="ic"></span><span class="tx"><b></b><i></i></span>';b.querySelector('.ic').textContent=ic;b.querySelector('b').textContent=label;const i=b.querySelector('i');if(sub)i.textContent=sub;else i.remove();b.onclick=fn||soon;return b}
function group(rows){const g=document.createElement('div');g.className='sg';rows.forEach(r=>g.appendChild(r));return g}
function head(t){const e=document.createElement('div');e.className='sh';e.textContent=t;return e}
function build(){
 const p=(tok&&jwt(tok))||{};const name=p.name||'Owner AI user';
 const box=document.getElementById('sbody');box.textContent='';
 const av=document.createElement('div');av.className='sav';av.textContent=(name.trim()[0]||'O').toUpperCase();
 const nm=document.createElement('div');nm.className='snm';nm.textContent=name;
 box.append(av,nm);
 box.append(head('My Owner AI'),group([row('\u{1F60A}','Personalization'),row('\u{1F9E0}','Memory'),row('\u{1F9E9}','Plugins')]));
 box.append(head('Account'),group([row('\u{1F4BC}','Workspace','Personal'),row('\u2728','Upgrade plan'),row('\u{1F4CA}','Usage and limits'),row('\u{1F46A}','Parental controls'),row('\u2709\uFE0F','Email',p.email||'',()=>{}),row('\u{1FAAA}','Age verification')]));
 const sel=document.createElement('select');sel.className='ssel';
 [['system','System (Default)'],['light','Light'],['dark','Dark']].forEach(a=>{const o=document.createElement('option');o.value=a[0];o.textContent=a[1];sel.appendChild(o)});
 sel.value=LS('oai_theme')||'system';sel.onchange=()=>{LS('oai_theme',sel.value);applyTheme()};sel.onclick=e=>e.stopPropagation();
 const apr=row('\u{1F313}','Appearance',null,()=>{});apr.appendChild(sel);
 const dots=document.createElement('div');dots.className='sdots';
 Object.keys(COL).forEach(k=>{const d=document.createElement('button');d.className='sdot';d.style.background=COL[k];d.setAttribute('aria-label',k);d.onclick=e=>{e.stopPropagation();LS('oai_accent',k);applyTheme();toast('Accent: '+k)};dots.appendChild(d)});
 const acr=row('\u{1F3A8}','Accent color',null,()=>{});acr.appendChild(dots);
 box.append(head(''),group([apr,acr]));
 box.append(head(''),group([
  row('\u2699\uFE0F','General'),row('\u{1F514}','Notifications'),row('\u{1F399}\uFE0F','Voice'),row('\u{1F6E1}\uFE0F','Safety & wellbeing'),row('\u{1F510}','Security and login'),row('\u{1F5A5}\uFE0F','Remote control'),
  row('\u{1F4BE}','Storage','Saved settings reset karo',()=>{LS('oai_theme',null);LS('oai_accent',null);applyTheme();build();toast('Settings reset ho gayi')}),
  row('\u{1F5C2}\uFE0F','Data controls','Chat saaf karo',()=>{reset();toast('Chat saaf ho gayi')}),
  row('\u{1F4E2}','Ads controls'),
  row('\u{1F41E}','Report bug',null,()=>window.open('https://github.com/Vikash1450/vikash1450.github.io/issues/new','_blank')),
  row('\u{1F512}','Privacy policy',null,()=>window.open('privacy.html','_blank')),
  row('\u2139\uFE0F','About','Owner AI \u2022 Developed by Vikash',()=>toast('Owner AI \u2014 Developed by Vikash'))]));
 const lo=row('\u21AA\uFE0F','Log out',null,()=>{document.getElementById('sets').hidden=true;logout('')});lo.classList.add('slo');box.append(head(''),group([lo]));
}
window.openSettings=()=>{build();const s=document.getElementById('sets');s.hidden=false;s.scrollTop=0};
document.getElementById('sback').onclick=()=>{document.getElementById('sets').hidden=true};
document.getElementById('setbtn').onclick=()=>{document.getElementById('about').hidden=true;window.openSettings()};
})();'''
p='index.html'
s=open(p,encoding='utf-8').read()
if 'id="sets"' in s:
    print('pehle se laga hai'); raise SystemExit
for n in ['</head>','</body>','<button id="out">Logout</button>']:
    if s.count(n)!=1:
        print('NAHI MILA:',n,s.count(n)); raise SystemExit
s=s.replace('</head>','<style>'+CSS+'</style>\n</head>')
s=s.replace('<button id="out">Logout</button>','<button id="setbtn">\u2699\uFE0F Settings</button>\n  <button id="out">Logout</button>')
s=s.replace('</body>',HTML+'<script>'+JS+'</script>\n</body>')
open(p,'w',encoding='utf-8').write(s)
print('OK')
