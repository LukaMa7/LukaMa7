import json, sys
src = sys.argv[1]  # live deck.json
d = json.load(open(src))
ids = json.load(open('ids.json'))
d['title'] = 'تطبيق الضوابط الأساسية للأمن السيبراني ECC-2:2024 بالتفصيل'
d['cover'] = 'cover'
d['order'] = ids
secs = json.load(open('sections.json'))
d['sections'] = {f's{i:02d}': {'description': desc, 'start': sid} for i, (sid, desc) in enumerate(secs)}
d['faces'] = {
    'alexandria': {'family': 'Alexandria', 'href': 'https://fonts.googleapis.com/css2?family=Alexandria:wght@400..800&display=swap'},
    'ibm-plex-sans-arabic': {'family': 'IBM Plex Sans Arabic', 'href': 'https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap'},
    'ibm-plex-mono': {'family': 'IBM Plex Mono', 'href': 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&display=swap'},
}
d.setdefault('designSystems', [])
json.dump(d, open('../deck_new/project/deck.json', 'w'), ensure_ascii=False, indent=2)
print(len(ids), list(d.keys()))
