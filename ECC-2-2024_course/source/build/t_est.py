import json, theme
from slides import *
d=json.load(open('extracted.json'))
for sid,r in d.items():
    if not sid.startswith('c') or sid=='closing' or sid=='cover': continue
    rows=r['tables'][0][1:]
    comp={'1':'gov','2':'def','3':'res','4':'tp'}[sid[1]]
    title=[x for x in r['text'] if x.startswith('h2:')][0][4:]
    hd,e=header('x',title,comp)
    g,e2=controls_grid([tuple(x)+('حد أدنى',) for x in rows],comp)
    print(sid, len(rows), int(e+32+e2))
