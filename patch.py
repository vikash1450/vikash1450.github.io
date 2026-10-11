s = open('index.html', encoding='utf-8').read()

def rep(old, new):
    global s
    assert s.count(old) == 1, 'nahi mila: ' + old[:40]
    s = s.replace(old, new)

CSS = r'''#sb{position:fixed;top:0;bottom:0;left:-82%;width:78%;max-width:320px;background:var(--bg);border-right:1px solid var(--line);z-index:20;padding:calc(env(safe-area-inset-top,0px) + 18px) 18px 18px;display:flex;flex-direction:column;transition:left .25s}
#sb.open{left:0}
#ov{position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:15}
#sb h2{font-family:Georgia,serif;font-size:30px;font-weight:500;margin:6px 0 22px}
.lab{color:var(--mute);margin:0 0 8px;font-size:14px}
#rl{list-style:none;margin:0;padding:0;flex:1;overflow-y:auto}
#rl li{display:flex;align-items:center;gap:8px;padding:11px 4px;cursor:pointer;font-size:16px}
#rl li span{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#rl li button{border:0;background:none;color:var(--mute);font-size:16px;cursor:pointer}
.sbf{display:flex;gap:10px;align-items:center;justify-content:space-between}
#nc{background:var(--fg);color:var(--bg);border:0;border-radius:24px;padding:13px 20px;font:inherit;font-size:16px;cursor:pointer}
#out2{background:var(--card);color:var(--fg);border:0;border-radius:24px;padding:13px 18px;font:inherit;font-size:15px;cursor:pointer}
</style>'''
rep('</style>', CSS)

HTML = r'''<div id="app" hidden>
<aside id="sb"><h2>Owner AI</h2><div class="lab">Recents</div><ul id="rl"></ul><div class="sbf"><button id="nc">+ New chat</button><button id="out2">Logout</button></div></aside>
<div id="ov" hidden></div>'''
rep('<div id="app" hidden>', HTML)

rep("$('menu').onclick=()=>{$('about').hidden=!$('about').hidden};", "$('menu').onclick=openSb;")
rep('function reset(){hist.length=0;', 'function reset(){cur=null;hist.length=0;')
rep("tok=c;$('login').hidden=true;", "tok=c;uid=p.sub||'u';loadChats();renderList();$('login').hidden=true;")
rep("w.textContent=a;hist.push({role:'assistant',content:a});", "w.textContent=a;hist.push({role:'assistant',content:a});saveChat();")

JS = r'''let chats=[],cur=null,uid='u';
const sb=$('sb');
function openSb(){sb.classList.add('open');$('ov').hidden=false}
function closeSb(){sb.classList.remove('open');$('ov').hidden=true}
function loadChats(){try{chats=JSON.parse(localStorage.getItem('oai_chats_'+uid)||'[]')}catch(e){chats=[]}}
function persist(){try{localStorage.setItem('oai_chats_'+uid,JSON.stringify(chats))}catch(e){}}
function saveChat(){
  if(!hist.length)return;
  if(!cur){cur=Date.now();chats.push({id:cur,title:hist[0].content.slice(0,30),msgs:[]})}
  chats.find(c=>c.id===cur).msgs=hist.slice();
  persist();renderList();
}
function openChat(id){
  const c=chats.find(x=>x.id===id);if(!c)return;
  reset();cur=id;$('empty').hidden=true;$('sug').hidden=true;
  c.msgs.forEach(m=>{hist.push(m);add(m.content,m.role==='user'?'me':'ai')});
  closeSb();
}
function renderList(){
  const ul=$('rl');ul.innerHTML='';
  chats.slice().reverse().forEach(c=>{
    const li=document.createElement('li'),sp=document.createElement('span'),x=document.createElement('button');
    sp.textContent=c.title;x.textContent='✕';x.setAttribute('aria-label','Delete');
    li.onclick=()=>openChat(c.id);
    x.onclick=e=>{e.stopPropagation();chats=chats.filter(k=>k.id!==c.id);persist();if(cur===c.id)reset();renderList()};
    li.appendChild(sp);li.appendChild(x);ul.appendChild(li);
  });
}
$('ov').onclick=closeSb;
$('nc').onclick=()=>{reset();closeSb()};
$('out2').onclick=()=>{closeSb();logout('')};
show(load());'''
rep('\nshow(load());\n', '\n' + JS + '\n')

open('index.html', 'w', encoding='utf-8').write(s)
print('Ho gaya!')
