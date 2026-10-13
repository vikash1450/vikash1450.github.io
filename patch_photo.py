PHOTO="""function pickPhoto(f){if(!f)return;const r=new FileReader();r.onload=()=>{const im=new Image();im.onload=()=>{const s=Math.min(1,1024/Math.max(im.width,im.height)),c=document.createElement('canvas');c.width=Math.round(im.width*s);c.height=Math.round(im.height*s);c.getContext('2d').drawImage(im,0,0,c.width,c.height);pendingImg=c.toDataURL('image/jpeg',0.8);$('photo').style.background='#dbe7ff';t.placeholder='Photo lag gayi - ab sawal likhiye';t.focus()};im.src=r.result};r.readAsDataURL(f)}
$('photo').onclick=()=>$('pic').click();
$('pic').onchange=e=>{pickPhoto(e.target.files[0]);e.target.value=''};"""
R=[
("let busy=false,tok=null;",
 "let busy=false,tok=null,pendingImg=null;"),
("q=q.trim();if(!q||busy||!tok)return;",
 "q=q.trim();if(!q&&pendingImg)q='Is photo ke baare mein batao.';if(!q||busy||!tok)return;"),
("busy=true;$('empty').hidden=true;$('sug').hidden=true;t.value='';",
 "busy=true;$('empty').hidden=true;$('sug').hidden=true;t.value='';const img=pendingImg;pendingImg=null;$('photo').style.background='';t.placeholder='Owner AI se poochiye';"),
("add(q,'me');hist.push({role:'user',content:q});",
 "const mb=add(q,'me');if(img){const im=document.createElement('img');im.src=img;im.style.cssText='display:block;max-width:100%;max-height:200px;border-radius:12px;margin-bottom:6px';mb.prepend(im)}hist.push({role:'user',content:q});"),
("body:JSON.stringify({messages:hist})",
 "body:JSON.stringify({messages:hist,image:img})"),
("$('f').onsubmit=e=>{e.preventDefault();ask(t.value)};",
 "$('f').onsubmit=e=>{e.preventDefault();ask(t.value)};\n"+PHOTO),
]
p='index.html'
s=open(p,encoding='utf-8').read()
for a,b in R:
    if s.count(a)!=1:
        print('NAHI MILA:',a[:40]); raise SystemExit
    s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s)
print('OK')
