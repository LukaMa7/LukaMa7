import json,re,sys,html
from html.parser import HTMLParser
D='../deck3/project'
order=json.load(open(D+'/deck.json'))['order']
def clean(t):
    t=html.unescape(t); t=re.sub(r'[‪-‮]','',t); return re.sub(r'\s+',' ',t).strip()
out={}
for sid in order:
    s=open(f'{D}/slides/{sid}.html',encoding='utf-8').read()
    m=re.search(r'<aside>(.*?)</aside>',s,re.S); notes=clean(m.group(1)) if m else ''
    body=re.sub(r'<aside>.*?</aside>','',s,flags=re.S)
    rec={'notes':notes}
    rows=[]
    for tm in re.finditer(r'<table.*?</table>',body,re.S):
        t=[]
        for tr in re.finditer(r'<tr.*?</tr>',tm.group(0),re.S):
            cells=[clean(re.sub(r'<[^>]+>',' ',c)) for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>',tr.group(0),re.S)]
            t.append(cells[::-1])
        rows.append(t)
    rec['tables']=rows
    rest=re.sub(r'<table.*?</table>',' [TABLE] ',body,flags=re.S)
    rest=re.sub(r'<(p|h1|h2|h3|li)[^>]*>(.*?)</\1>',lambda m:'\n'+m.group(1)+': '+clean(re.sub(r'<[^>]+>','',m.group(2)))+'\n',rest,flags=re.S)
    rest=re.sub(r'<[^>]+>',' ',rest)
    rec['text']=[l.strip() for l in rest.split('\n') if l.strip() and l.strip()!='[TABLE]' or l.strip()=='[TABLE]']
    rec['text']=[x for x in rec['text'] if x]
    out[sid]=rec
json.dump(out,open('extracted.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out))
