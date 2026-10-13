# -*- coding: utf-8 -*-
CSS2=r'''.sck{margin-left:auto;width:22px;height:22px;accent-color:var(--blue);flex:none}
.sinfo{color:var(--mute);font-size:14px;line-height:1.5;margin:12px 8px}
.sfield{display:flex;flex-direction:column;gap:6px;padding:14px 16px;border-bottom:1px solid var(--bg)}
.sfield label{font-size:13px;color:var(--mute)}
.sfield input,.sfield textarea{background:var(--bg);color:var(--fg);border:1px solid var(--line);border-radius:10px;padding:10px;font:inherit;width:100%;box-sizing:border-box}
.sdel{background:none;border:0;color:#e5484d;font-size:18px;margin-left:auto;cursor:pointer}
.sdanger .tx b{color:#e5484d}
.si .tx{min-width:0}
.sg .si:has(.ssel) .tx{flex:1}'''
JS2=r'''/*settings-v2*/(function(){
const LS=(k,v)=>{try{if(v===undefined)return localStorage.getItem(k);v===null?localStorage.removeItem(k):localStorage.setItem(k,v)}catch(e){return null}};
const COL={Blue:'#2f6bff',Green:'#1aa260',Purple:'#7b4dff',Orange:'#f07a1a',Pink:'#e0407a'};
const E=(tag,cls,txt)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(txt!==undefined)e.textContent=txt;return e};
const vl=()=>LS('oai_vlang')||'hi-IN';
window.oaiVLang=vl;
let tm,bt=null,unlocked=false,view='list';
function toast(m){const e=$('toast');e.textContent=m;e.hidden=false;clearTimeout(tm);tm=setTimeout(()=>{e.hidden=true},2400)}
function applyAll(){
  const r=document.documentElement,th=LS('oai_theme')||'system';
  if(th==='system')r.removeAttribute('data-theme');else r.setAttribute('data-theme',th);
  r.style.setProperty('--blue',COL[LS('oai_accent')||'Blue']||COL.Blue);
  document.body.style.zoom={small:'0.9',medium:'1',large:'1.15'}[LS('oai_font')||'medium'];
  const ph=$('photo'),mc=$('mic'),sg=$('sug');
  if(ph)ph.style.display=LS('oai_pl_photo')==='0'?'none':'';
  if(mc)mc.style.display=LS('oai_pl_mic')==='0'?'none':'';
  if(sg)sg.style.display=LS('oai_sug')==='0'?'none':'';
}
function breakTimer(){clearInterval(bt);if(LS('oai_break')==='1')bt=setInterval(()=>toast('Thoda break lo, aankhon ko aaram do \u{1F60A}'),30*60*1000)}
function memList(){try{const a=JSON.parse(LS('oai_mem')||'[]');return Array.isArray(a)?a:[]}catch(e){return []}}
const today=()=>new Date().toISOString().slice(0,10);
function getUse(){let u;try{u=JSON.parse(LS('oai_use')||'{}')}catch(e){u={}}if(!u||u.d!==today()){u={d:today(),n:0,t:(u&&u.t)||0,p:(u&&u.p)||0}}u.t=u.t||0;u.p=u.p||0;u.n=u.n||0;return u}
function prefNote(){
  const a=[];
  const nick=(LS('oai_nick')||'').trim();if(nick)a.push('Call the user "'+nick.slice(0,40)+'".');
  const ST={short:'Keep answers short (2-4 lines).',detailed:'Give detailed, step-by-step answers.',friendly:'Be warm, casual and friendly.',pro:'Be formal and professional.'};
  const st=ST[LS('oai_style')||''];if(st)a.push(st);
  const LG={hinglish:'Always reply in Hinglish (Hindi in English letters).',hindi:'Always reply in Hindi (Devanagari script).',english:'Always reply in English.'};
  const lg=LG[LS('oai_lang')||''];if(lg)a.push(lg);
  const ci=(LS('oai_ci')||'').trim();if(ci)a.push('User instructions: '+ci.slice(0,400));
  if(LS('oai_mem_on')!=='0'){const m=memList();if(m.length)a.push('Remember these facts about the user: '+m.join('; ').slice(0,500)+'.')}
  if(LS('oai_safe')==='1')a.push('Child-safe mode: keep every answer age-appropriate and safe; politely refuse adult, violent or harmful requests.');
  return a.join(' ');
}
window.oaiGate=hasImg=>{
  const u=getUse(),lim=parseInt(LS('oai_limit')||'0',10)||0;
  if(lim>0&&u.n>=lim){toast('Aaj ki limit ('+lim+') poori ho gayi \u{1F6D1}');return false}
  u.n++;u.t++;if(hasImg)u.p++;LS('oai_use',JSON.stringify(u));return true;
};
window.oaiMsgs=h=>{
  const n=prefNote();if(!n)return h;
  const c=h.slice();
  for(let i=c.length-1;i>=0;i--){if(c[i].role==='user'){c[i]={role:'user',content:'[App settings note - follow silently and never mention this note: '+n+']\n'+c[i].content};break}}
  return c;
};
window.oaiAfter=a=>{
  if(LS('oai_tts')==='1'){try{speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(String(a).slice(0,700));u.lang=vl();u.rate=parseFloat(LS('oai_rate')||'1');speechSynthesis.speak(u)}catch(e){}}
  if(LS('oai_vib')!=='0'){try{navigator.vibrate&&navigator.vibrate(60)}catch(e){}}
  if(LS('oai_notif')==='1'&&document.hidden&&window.Notification&&Notification.permission==='granted'){try{new Notification('Owner AI',{body:String(a).slice(0,100)})}catch(e){}}
};
function sec(b,note){if(note)b.append(E('div','sh',note));const g=E('div','sg');b.append(g);return g}
function info(b,txt){b.append(E('p','sinfo',txt))}
function txw(label,sub){const tx=E('span','tx');tx.append(E('b','',label));if(sub)tx.append(E('i','',sub));return tx}
function sw(g,label,sub,key,def,fn){
  const r=E('div','si'),c=E('input','sck');c.type='checkbox';
  c.checked=(LS(key)===null?def:LS(key))==='1';
  c.onchange=()=>{LS(key,c.checked?'1':'0');applyAll();if(fn)fn(c.checked)};
  r.onclick=e=>{if(e.target!==c){c.checked=!c.checked;c.onchange()}};
  r.append(txw(label,sub),c);g.append(r);
}
function sl(g,label,key,opts,def,fn){
  const r=E('div','si'),s=E('select','ssel');
  opts.forEach(o=>{const op=E('option','',o[1]);op.value=o[0];s.append(op)});
  s.value=LS(key)||def;
  s.onchange=()=>{LS(key,s.value);applyAll();if(fn)fn(s.value)};
  s.onclick=e=>e.stopPropagation();
  r.append(txw(label),s);g.append(r);
}
function fld(g,label,key,ph,multi,type){
  const w=E('div','sfield'),i=E(multi?'textarea':'input');
  if(multi)i.rows=4;else i.type=type||'text';
  const tmp=/_(tmp|try)$/.test(key);
  i.placeholder=ph||'';i.value=tmp?'':(LS(key)||'');
  i.oninput=()=>{if(!tmp)LS(key,i.value)};
  w.append(E('label','',label),i);g.append(w);return i;
}
function btn(g,label,sub,fn,danger){
  const r=E('div','si'+(danger?' sdanger':''));r.append(txw(label,sub));r.onclick=fn;g.append(r);
}
function showPanel(title,fn){
  view=title;const b=$('sbody');b.textContent='';
  const h=E('div','snm',title);h.style.fontSize='20px';b.append(h);fn(b);
}
const P={};
P.pers=b=>{
  const g=sec(b,'Owner AI aapko kaise jaane');
  fld(g,'Aapka naam / nickname','oai_nick','Jaise: Vikash');
  sl(g,'Jawab ka style','oai_style',[['','Normal'],['short','Chhota'],['detailed','Detail mein'],['friendly','Friendly'],['pro','Professional']],'');
  sl(g,'Jawab ki bhasha','oai_lang',[['','Jaise main likhun'],['hinglish','Hinglish'],['hindi','Hindi'],['english','English']],'');
  fld(g,'Apni khaas instructions','oai_ci','Jaise: Mujhe examples ke saath samjhao',true);
  info(b,'Ye sab har sawal ke saath chupke se Owner AI ko bheji jaati hain.');
};
P.mem=b=>{
  const g=sec(b);
  sw(g,'Memory on','AI aapki baatein yaad rakhe','oai_mem_on','1');
  const box=E('div','sg');b.append(E('div','sh','Yaad rakhi hui baatein'),box);
  function render(){
    box.textContent='';const m=memList();
    if(!m.length)box.append(E('p','sinfo','Abhi kuch save nahi hai.'));
    m.forEach((x,i)=>{const r=E('div','si');r.append(E('span','tx',x));const d=E('button','sdel','\u2715');d.onclick=()=>{const a=memList();a.splice(i,1);LS('oai_mem',JSON.stringify(a));render()};r.append(d);box.append(r)});
  }
  render();
  const g2=sec(b,'Nayi baat jodo');
  const i=fld(g2,'Jaise: Main Delhi mein rehta hun','oai_mem_tmp','');i.value='';LS('oai_mem_tmp',null);
  btn(g2,'\u2795 Jodo',null,()=>{const v=i.value.trim();if(!v)return;const a=memList();a.push(v.slice(0,120));LS('oai_mem',JSON.stringify(a.slice(-20)));i.value='';LS('oai_mem_tmp',null);render()});
  btn(g2,'Saari memory mitao',null,()=>{LS('oai_mem',null);render();toast('Memory saaf ho gayi')},true);
};
P.plug=b=>{
  const g=sec(b,'Features on / off');
  sw(g,'\u{1F4F7} Photo bhejna','Photo wala button dikhao','oai_pl_photo','1');
  sw(g,'\u{1F3A4} Bolkar poochna','Mic wala button dikhao','oai_pl_mic','1');
  sw(g,'\u{1F4A1} Sujhav wale buttons','Home par 3 sujhav dikhao','oai_sug','1');
};
P.ws=b=>{
  const g=sec(b);
  fld(g,'Workspace ka naam','oai_ws','Personal');
  info(b,'Abhi Owner AI sirf aapke personal use ke liye hai. Team workspace abhi nahi hai.');
};
P.plan=b=>{
  info(b,'\u2705 Owner AI abhi poori tarah free hai: chat, photo samajhna, voice, sab. Paid plan abhi nahi hai.');
  const g=sec(b,'Dost ko batao');
  btn(g,'\u{1F4E4} App link bhejo',null,()=>{const u='https://vikash1450.github.io/owner-ai.apk';if(navigator.share)navigator.share({title:'Owner AI',text:'Owner AI app:',url:u}).catch(()=>{});else{try{navigator.clipboard.writeText(u);toast('Link copy ho gaya')}catch(e){}}});
};
P.use=b=>{
  const u=getUse(),g=sec(b,'Aapka istemaal');
  btn(g,'Aaj ke sawal',String(u.n),()=>{});
  btn(g,'Ab tak ke sawal',String(u.t),()=>{});
  btn(g,'Ab tak ki photos',String(u.p),()=>{});
  const g2=sec(b,'Roz ki limit');
  sl(g2,'Roz kitne sawal','oai_limit',[['0','Koi limit nahi'],['20','20'],['50','50'],['100','100'],['200','200']],'0');
  btn(g2,'Ginti zero karo',null,()=>{LS('oai_use',null);showPanel('Usage and limits',P.use)},true);
};
P.par=b=>{
  const has=!!LS('oai_pin');
  info(b,has?'\u{1F512} PIN laga hua hai. Settings kholne ke liye PIN lagega.':'PIN lagane par Settings kholne ke liye 4 ank ka PIN chahiye. Ye simple lock hai, bachchon ke liye accha hai.');
  const g=sec(b);
  if(has){btn(g,'PIN hatao',null,()=>{LS('oai_pin',null);toast('PIN hat gaya');showPanel('Parental controls',P.par)},true)}
  else{
    const i=fld(g,'4 ank ka PIN','oai_pin_tmp','1234',false,'password');i.inputMode='numeric';i.maxLength=4;i.value='';LS('oai_pin_tmp',null);
    btn(g,'\u{1F512} PIN lagao',null,()=>{if(!/^\d{4}$/.test(i.value)){toast('4 ank daalo');return}LS('oai_pin',i.value);LS('oai_pin_tmp',null);unlocked=true;toast('PIN lag gaya');showPanel('Parental controls',P.par)});
  }
  const g2=sec(b,'Bachchon ke liye');
  sw(g2,'Safe mode','Jawab bachchon ke layak rahein','oai_safe','0');
};
P.age=b=>{
  const g=sec(b,'Umar');
  const i=fld(g,'Aapka janm varsh','oai_birth','Jaise: 2005',false,'number');
  btn(g,'Save karo',null,()=>{const y=parseInt(i.value,10),a=new Date().getFullYear()-y;if(!y||a<5||a>110){toast('Sahi saal daalo');return}if(a<18){LS('oai_safe','1');toast('18 se kam: Safe mode on kar diya')}else toast('Save ho gaya');});
  info(b,'Ye aapki batayi hui umar hai, asli verification nahi. 18 se kam hone par Safe mode apne aap on ho jata hai.');
};
P.gen=b=>{
  const g=sec(b);
  sl(g,'Akshar ka size','oai_font',[['small','Chhota'],['medium','Normal'],['large','Bada']],'medium');
  sw(g,'Sujhav wale buttons','Home par 3 sujhav dikhao','oai_sug','1');
};
P.not=b=>{
  const g=sec(b);
  sw(g,'Jawab aane par vibrate','Chhota vibration','oai_vib','1');
  sw(g,'Background mein alert','App background mein ho tab jawab ka alert','oai_notif','0',on=>{if(on&&window.Notification&&Notification.permission==='default')Notification.requestPermission()});
  info(b,'Alert tabhi aata hai jab app khula ho par screen ke peeche ho. Band app par alert nahi aata.');
};
P.voice=b=>{
  const g=sec(b);
  sw(g,'Jawab bolkar sunao','Har jawab awaaz mein','oai_tts','0');
  sl(g,'Awaaz ki bhasha','oai_vlang',[['hi-IN','Hindi'],['en-IN','English (India)'],['en-US','English (US)']],'hi-IN');
  sl(g,'Bolne ki raftaar','oai_rate',[['0.8','Dheemi'],['1','Normal'],['1.2','Tez']],'1');
  btn(g,'\u25B6 Awaaz test karo',null,()=>{try{speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(vl()==='hi-IN'?'Namaste, main Owner AI hun':'Hello, I am Owner AI');u.lang=vl();u.rate=parseFloat(LS('oai_rate')||'1');speechSynthesis.speak(u)}catch(e){toast('Awaaz is phone par nahi chali')}});
};
P.safe=b=>{
  const g=sec(b);
  sw(g,'Safe mode','Jawab safe aur age-appropriate rahein','oai_safe','0');
  sw(g,'Break reminder','Har 30 minute mein yaad dilao','oai_break','0',breakTimer);
  info(b,'Zyada der screen dekhne se aankhein thakti hain. Break reminder app khula rehne par hi chalta hai.');
};
P.sec=b=>{
  const p=(typeof tok!=='undefined'&&tok&&jwt(tok))||{};
  const g=sec(b,'Login');
  btn(g,'Email',p.email||'-',()=>{});
  btn(g,'Login ka samay',p.exp?new Date(p.exp*1000).toLocaleString():'-',()=>{});
  const g2=sec(b);
  btn(g2,'Log out',null,()=>{$('sets').hidden=true;logout('')});
  btn(g2,'Phone se saara Owner AI data mitao','Settings, memory, login sab',()=>{try{Object.keys(localStorage).filter(k=>k.indexOf('oai_')===0).forEach(k=>localStorage.removeItem(k))}catch(e){}applyAll();$('sets').hidden=true;logout('');toast('Saara data mit gaya')},true);
};
P.rem=b=>{
  info(b,'Web app se doosre phone ya computer ko control karna possible nahi hai. Lekin aap app ka link doosre device par bhej sakte ho.');
  const g=sec(b);
  btn(g,'\u{1F4E4} App link bhejo',null,()=>{const u='https://vikash1450.github.io/owner-ai.apk';if(navigator.share)navigator.share({title:'Owner AI',url:u}).catch(()=>{});else{try{navigator.clipboard.writeText(u);toast('Link copy ho gaya')}catch(e){}}});
  btn(g,'\u{1F310} Website link copy karo',null,()=>{try{navigator.clipboard.writeText('https://vikash1450.github.io');toast('Link copy ho gaya')}catch(e){toast('Copy nahi hua')}});
};
P.sto=b=>{
  let n=0;try{Object.keys(localStorage).filter(k=>k.indexOf('oai_')===0).forEach(k=>{n+=k.length+(localStorage.getItem(k)||'').length})}catch(e){}
  const g=sec(b,'Saved data');
  btn(g,'Phone mein jagah',(n/1024).toFixed(1)+' KB',()=>{});
  btn(g,'Settings reset karo','Login nahi hatega',()=>{try{Object.keys(localStorage).filter(k=>k.indexOf('oai_')===0&&k!=='oai_tok').forEach(k=>localStorage.removeItem(k))}catch(e){}applyAll();toast('Settings reset ho gayi');showPanel('Storage',P.sto)},true);
};
P.data=b=>{
  const g=sec(b);
  btn(g,'\u{1F4CB} Chat copy karo',null,()=>{const t2=hist.map(m=>(m.role==='user'?'Main: ':'Owner AI: ')+m.content).join('\n\n');try{navigator.clipboard.writeText(t2||'(chat khali hai)');toast('Chat copy ho gayi')}catch(e){toast('Copy nahi hua')}});
  btn(g,'Chat saaf karo',null,()=>{reset();toast('Chat saaf ho gayi')},true);
};
P.ads=b=>{info(b,'Owner AI mein koi ads nahi hain, isliye ads ki koi setting bhi nahi hai.')};
const NM={pers:'Personalization',mem:'Memory',plug:'Plugins',ws:'Workspace',plan:'Upgrade plan',use:'Usage and limits',par:'Parental controls',age:'Age verification',gen:'General',not:'Notifications',voice:'Voice',safe:'Safety & wellbeing',sec:'Security and login',rem:'Remote control',sto:'Storage',data:'Data controls',ads:'Ads controls'};
function go(k){return()=>showPanel(NM[k],P[k])}
function row(ic,label,sub,fn){
  const b=E('div','si'),i=E('span','ic',ic);b.append(i,txw(label,sub));b.onclick=fn||(()=>{});return b;
}
function grp(rows){const g=E('div','sg');rows.forEach(r=>g.append(r));return g}
function head(t){return E('div','sh',t)}
function showList(){
  view='list';
  const p=(typeof tok!=='undefined'&&tok&&jwt(tok))||{},name=p.name||'Owner AI user',box=$('sbody');
  box.textContent='';
  const av=E('div','sav',(name.trim()[0]||'O').toUpperCase()),nm=E('div','snm',name);
  box.append(av,nm);
  box.append(head('My Owner AI'),grp([row('\u{1F60A}','Personalization',null,go('pers')),row('\u{1F9E0}','Memory',null,go('mem')),row('\u{1F9E9}','Plugins',null,go('plug'))]));
  box.append(head('Account'),grp([row('\u{1F4BC}','Workspace',LS('oai_ws')||'Personal',go('ws')),row('\u2728','Upgrade plan',null,go('plan')),row('\u{1F4CA}','Usage and limits',null,go('use')),row('\u{1F46A}','Parental controls',null,go('par')),row('\u2709\uFE0F','Email',p.email||'',()=>{}),row('\u{1FAAA}','Age verification',null,go('age'))]));
  const sel=E('select','ssel');
  [['system','System (Default)'],['light','Light'],['dark','Dark']].forEach(a=>{const o=E('option','',a[1]);o.value=a[0];sel.append(o)});
  sel.value=LS('oai_theme')||'system';sel.onchange=()=>{LS('oai_theme',sel.value);applyAll()};sel.onclick=e=>e.stopPropagation();
  const apr=row('\u{1F313}','Appearance');apr.append(sel);
  const dots=E('div','sdots');
  Object.keys(COL).forEach(k=>{const d=E('button','sdot');d.style.background=COL[k];d.setAttribute('aria-label',k);d.onclick=e=>{e.stopPropagation();LS('oai_accent',k);applyAll();toast('Accent: '+k)};dots.append(d)});
  const acr=row('\u{1F3A8}','Accent color');acr.append(dots);
  box.append(head(''),grp([apr,acr]));
  box.append(head(''),grp([
    row('\u2699\uFE0F','General',null,go('gen')),row('\u{1F514}','Notifications',null,go('not')),row('\u{1F399}\uFE0F','Voice',null,go('voice')),row('\u{1F6E1}\uFE0F','Safety & wellbeing',null,go('safe')),row('\u{1F510}','Security and login',null,go('sec')),row('\u{1F5A5}\uFE0F','Remote control',null,go('rem')),
    row('\u{1F4BE}','Storage',null,go('sto')),row('\u{1F5C2}\uFE0F','Data controls',null,go('data')),row('\u{1F4E2}','Ads controls',null,go('ads')),
    row('\u{1F41E}','Report bug',null,()=>window.open('https://github.com/Vikash1450/vikash1450.github.io/issues/new','_blank')),
    row('\u{1F512}','Privacy policy',null,()=>window.open('privacy.html','_blank')),
    row('\u2139\uFE0F','About','Owner AI \u2022 Developed by Vikash',()=>toast('Owner AI \u2014 Developed by Vikash'))]));
  const lo=row('\u21AA\uFE0F','Log out',null,()=>{$('sets').hidden=true;logout('')});lo.classList.add('slo');box.append(head(''),grp([lo]));
}
function showLock(){
  view='lock';const b=$('sbody');b.textContent='';
  b.append(E('div','snm','\u{1F512} PIN daalo'));
  const g=sec(b),i=fld(g,'4 ank ka PIN','oai_pin_try','',false,'password');i.inputMode='numeric';i.maxLength=4;i.value='';LS('oai_pin_try',null);
  btn(g,'Kholo',null,()=>{if(i.value===LS('oai_pin')){unlocked=true;showList()}else{toast('Galat PIN');i.value=''}});
}
window.openSettings=()=>{const s=$('sets');s.hidden=false;s.scrollTop=0;if(LS('oai_pin')&&!unlocked)showLock();else showList()};
$('sback').onclick=()=>{if(view!=='list'&&view!=='lock')showList();else $('sets').hidden=true};
$('setbtn').onclick=()=>{$('about').hidden=true;window.openSettings()};
applyAll();breakTimer();
})();
'''
p='index.html'
s=open(p,encoding='utf-8').read()
if '/*settings-v2*/' in s:
    print('pehle se laga hai'); raise SystemExit
A="<script>(function(){\nconst LS=(k,v)=>"
i=s.find(A)
if i<0:
    print('NAHI MILA: purani settings'); raise SystemExit
E_="})();</script>"
j=s.find(E_,i)
if j<0:
    print('NAHI MILA: purani settings ka end'); raise SystemExit
s=s[:i]+'<script>'+JS2+'</script>'+s[j+len(E_):]
R=[
("if(!q||busy||!tok)return;",
 "if(!q||busy||!tok)return;if(window.oaiGate&&!window.oaiGate(!!pendingImg))return;"),
("body:JSON.stringify({messages:hist,image:img})",
 "body:JSON.stringify({messages:(window.oaiMsgs?window.oaiMsgs(hist):hist),image:img})"),
("w.textContent=a;hist.push({role:'assistant',content:a});",
 "w.textContent=a;hist.push({role:'assistant',content:a});window.oaiAfter&&window.oaiAfter(a);"),
("$('mic').onclick=()=>{try{rec.start()}catch(e){}}",
 "$('mic').onclick=()=>{try{rec.lang=window.oaiVLang?window.oaiVLang():'hi-IN';rec.start()}catch(e){}}"),
("</head>","<style>"+CSS2+"</style>\n</head>"),
]
for a,b in R:
    if s.count(a)!=1:
        print('NAHI MILA:',a[:45],'(mile:',s.count(a),')'); raise SystemExit
    s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s)
print('OK')
