import pathlib,json,hashlib,zipfile,mimetypes,re,sys,shutil
root=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '.independent-review/windows/resources/template/data/stickers');out=pathlib.Path(sys.argv[2] if len(sys.argv)>2 else 'xinlian/dist/sticker-packs');out.mkdir(parents=True,exist_ok=True)
source=json.loads((root/'index.json').read_text(encoding='utf8'));groups={};names={'blue archive':('starlit-blue-archive','蔚蓝档案'),'mygo':('starlit-mygo','MyGO'),'超时空辉夜姬表情包':('starlit-kaguya','超时空辉夜姬'),'stolen':('starlit-reactions','通用反应')}
for row in source:
 f=root/row['file']
 if not f.is_file():continue
 top=row['file'].split('/')[0];pack,title=names[top];data=f.read_bytes();sha=hashlib.sha256(data).hexdigest();asset={'id':sha[:24],'file':'assets/'+sha[:24]+f.suffix.lower(),'sha256':sha,'bytes':len(data),'mime':{'.gif':'image/gif','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.webp':'image/webp'}[f.suffix.lower()],'label':re.sub(r'[_ ]+[A-Fa-f0-9]{6,}$','',row.get('desc',f.stem)),'tags':list(dict.fromkeys(row.get('emotions',[])+row.get('tags',[]))),'source':top};groups.setdefault(pack,{'id':pack,'title':title,'assets':{}})['assets'].setdefault(asset['id'],(asset,f))
catalog={'version':1,'packs':[]}
for pack,g in groups.items():
 assets=[v[0] for v in g['assets'].values()];manifest={'format':'xinlian-sticker-pack','version':1,'id':pack,'title':g['title'],'assets':assets};target=out/(pack+'.xlp')
 with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
  z.writestr(zipfile.ZipInfo('manifest.json',(2026,1,1,0,0,0)),json.dumps(manifest,ensure_ascii=False,separators=(',',':')))
  for a,f in g['assets'].values():
   with z.open(zipfile.ZipInfo(a['file'],(2026,1,1,0,0,0)),'w') as dest, f.open('rb') as src:shutil.copyfileobj(src,dest)
 sha=hashlib.file_digest(target.open('rb'),'sha256').hexdigest();catalog['packs'].append({'id':pack,'title':g['title'],'bytes':target.stat().st_size,'contentBytes':sum(a['bytes'] for a in assets),'sha256':sha,'url':'https://github.com/lind000721/bot-/releases/download/sticker-assets-v1/'+pack+'.xlp','assets':assets})
(out/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':')),encoding='utf8');
if pathlib.Path('xinlian/web').is_dir():shutil.copyfile(out/'catalog.json','xinlian/web/sticker-catalog.json')
print([(p['title'],len(p['assets']),p['bytes']) for p in catalog['packs']])

