# usage: python3 dumptext.py <slides_dir> <ids.json> <out.md>
import sys, json, re, html
d, ids, out = sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3]
o = []
for n, sid in enumerate(ids, 1):
    h = open(f'{d}/{sid}.html', encoding='utf-8').read()
    notes = ''
    m = re.search(r'<aside>(.*?)</aside>', h, re.S)
    if m:
        notes = m.group(1); h = h.replace(m.group(0), '')
    # table cells / grid cells -> separators
    h = re.sub(r'</(td|th)>', ' | ', h)
    h = re.sub(r'</(tr|p|h1|h2|h3|div)>', '\n', h)
    txt = html.unescape(re.sub(r'<[^>]+>', '', h)).replace('‫', '')
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    o.append(f'## {n} · {sid}\n' + '\n'.join(lines) + f'\n\n[ملاحظات المدرب] {html.unescape(notes)}\n')
open(out, 'w', encoding='utf-8').write('\n'.join(o))
print(len(ids))
