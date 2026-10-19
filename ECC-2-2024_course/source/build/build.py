import json, os, sys, importlib
import theme
from theme import *
import slides as T
import mocks

OUT = '../deck_new/project'
ASSETS = json.load(open('assets.json', encoding='utf-8')) if os.path.exists('assets.json') else {}

def img_box(topic, w, h, fit='contain'):
    a = ASSETS.get(topic)
    src = f' src="{a["url"]}"' if a and a.get('url') else ''
    alt = esc(a['alt']) if a and a.get('alt') else esc(topic)
    if fit == 'cover':
        return f'<img{src} alt="{alt}" style="width:{w}px;height:{h}px;object-fit:cover;border-radius:18px">'
    return (f'<div style="width:{w}px;height:{h}px;background:{INK};border-radius:18px;padding:16px;display:flex;align-items:center;justify-content:center">'
            f'<img{src} alt="{alt}" style="width:{w - 32}px;height:{h - 32}px;object-fit:contain;border-radius:6px"></div>')

def credit_for(topics):
    sites = [ASSETS.get(tp, {}).get('site', 'Wikimedia Commons') for tp in topics]
    parts = []
    for tp in topics:
        a = ASSETS.get(tp, {})
        p = f'{a.get("author", "؟")} · {a.get("license", "؟")}'
        if len(set(sites)) > 1:
            p += f' · {a.get("site", "")}'
        parts.append(p)
    lead = 'صورة توضيحية من الإنترنت، ليست دليلاً صادراً عن جهة' if len(topics) == 1 else 'صور توضيحية من الإنترنت، ليست أدلة صادرة عن جهة'
    tail = f' · المصدر: {sites[0]}' if len(set(sites)) == 1 else ''
    return f'{lead} · ' + ' | '.join(parts) + tail

def media(sp):
    m = sp['media']
    if m['type'] == 'img':
        h = m.get('h', 520)
        return img_box(m['topic'], mocks.MW, h, m.get('fit', 'contain')), h, credit_for([m['topic']])
    if m['type'] == 'img2':
        h = m.get('h', 520)
        wt = m.get('weights', [1] * len(m['topics']))
        fits = m.get('fits', [m.get('fit', 'cover')] * len(m['topics']))
        ws = [int((mocks.MW - 20) * x / sum(wt)) for x in wt]
        boxes = ''.join(img_box(tp, w, h, f) for tp, w, f in zip(m['topics'], ws, fits))
        return f'<div style="display:flex;flex-direction:row-reverse;gap:20px">{boxes}</div>', h, credit_for(m['topics'])
    if m['type'] == 'mock':
        h, e = m['fn']()
        return h, e, 'نموذج دليل تدريبي من إعداد الكورس · البيانات والأسماء افتراضية'
    raise ValueError(m)

def render(kind, sp):
    if kind == 'evidence':
        mh, me, cr = media(sp)
        if sp.get('credit'):
            cr = sp['credit']
        return T.evidence(sp, mh, me, cr)
    if kind == 'answer':
        return T.tablepage(sp)
    if kind == 'raw':
        return sp['fn']()
    return getattr(T, kind)(sp)

# module divider items -> the slide each one points to (control units map by code)
REFS = {'m0': ['f-what', 'f-cia', 'f-risk', 'f-controls', 'f-compliance', 'f-evidence', 'f-sample', 'g-id', 'exA'],
        'm1': ['ecc-what', 'ecc-scope', 'ecc-structure', 'ecc-family', 'layers', 'doc-pyramid', 'ex1'],
        'm2': ['prog-phases', 'prog-deps', 'prog-waves', 'raci', 'evidence-repo', 'ex2'],
        'm7': ['sus-why', 'docs-pack', 'review-calendar', 'kpis', 'readiness', 'pitfalls', 'ex7', 'case-entity'],
        'm8': ['quiz-a', 'quiz-b', 'perf-intro', 'perf-e1', 'next-steps', 'closing']}
SUBKINDS = ('sub_intro', 'controls', 'evidence')
STAGEOF = {'judge': 'evidence'}  # slides that belong to a subcomponent's evidence step

def navigate(allS):
    """Per slide: unit number, subcomponent run and stage, slide number; also the outline sections"""
    ids = [sp['id'] for _, sp in allS]
    assert len(ids) == len(set(ids))
    theme.POS.clear()
    theme.POS.update({i: n + 1 for n, i in enumerate(ids)})
    runs, cur, mod = [], None, '00'
    navs = []
    for kind, sp in allS:
        kind = sp.get('stage') or STAGEOF.get(kind, kind)
        if kind == 'module':
            mod = sp['num']
        if kind == 'sub_intro':
            cur = dict(code=sp['code'], name=sp['name'], mod=mod, kinds=[])
            runs.append(cur)
        elif kind not in SUBKINDS:
            cur = None
        if cur is not None:
            cur['kinds'].append(kind)
        navs.append(dict(mod=mod, run=cur, kind=kind, pos=theme.POS[sp['id']]))
    per_mod = {}
    for r in runs:
        per_mod.setdefault(r['mod'], []).append(r)
    for r in runs:
        r['k'] = per_mod[r['mod']].index(r) + 1
        r['n'] = len(per_mod[r['mod']])
    seen = {}
    for nv in navs:
        r = nv.pop('run')
        if r is None:
            nv['sub'] = None
            continue
        key = (id(r), nv['kind'])
        seen[key] = seen.get(key, 0) + 1
        stages = [k for k in SUBKINDS if k in r['kinds']]
        nv['sub'] = dict(code=r['code'], name=r['name'], k=r['k'], n=r['n'], stages=stages, kind=nv['kind'],
                         idx=seen[key], cnt=r['kinds'].count(nv['kind']))
    for kind, sp in allS:
        if kind == 'module':
            refs = REFS.get(sp['id']) or ['i' + c for c, _ in sp.get('items', [])]
            sp['refs'] = [theme.POS.get(x) for x in refs]
            theme.MODITEMS[sp['num']] = (sp['id'], sp['title'], sp.get('items', []))
    # outline: one section per unit, and per subcomponent / exercise inside the control units
    secs = []
    for (kind, sp), nv in zip(allS, navs):
        if kind == 'module' or sp['id'] == 'cover':
            secs.append((sp['id'], SECDESC[nv['mod']]))
        elif kind == 'sub_intro':
            secs.append((sp['id'], f'الوحدة {nv["mod"]} · المكوّن {sp["code"]}: {sp["name"]}'))
        elif kind == 'exercise' and nv['mod'] in ('04', '05', '06', '07'):
            secs.append((sp['id'], f'الوحدة {nv["mod"]} · {sp["eyebrow"].split(" · ")[0]} وحله'))
    return ids, navs, secs

SECDESC = {'00': 'مقدمة الكورس: لمن هو، والأهداف، وخريطة الوحدات، وفهرس المكونات، وطريقة قراءة الشرائح',
           '01': 'الوحدة 01: مفاهيم أساسية للمبتدئين، والأدلة، وقاموس المصطلحات',
           '02': 'الوحدة 02: أساسيات ECC-2:2024 والنطاق والبنية والطبقات الأربع',
           '03': 'الوحدة 03: بناء برنامج التطبيق والأدوار وسجل الأدلة',
           '04': 'الوحدة 04: الحوكمة، المكونات الفرعية 1-1 إلى 1-10',
           '05': 'الوحدة 05: التعزيز (1)، المكونات الفرعية 2-1 إلى 2-8',
           '06': 'الوحدة 06: التعزيز (2)، المكونات الفرعية 2-9 إلى 2-15',
           '07': 'الوحدة 07: الصمود والأطراف الخارجية والحوسبة السحابية: 3-1 و4-1 و4-2',
           '08': 'الوحدة 08: الاستدامة والمؤشرات والجاهزية لتقييم الهيئة',
           '09': 'الوحدة 09: الاختبار النهائي وخطة ما بعد الكورس والختام'}

def main(mods):
    allS = []
    for mname in mods:
        mod = importlib.import_module(mname)
        allS.extend(mod.S)
    os.makedirs(OUT + '/slides', exist_ok=True)
    ids, navs, secs = navigate(allS)
    json.dump(secs, open('sections.json', 'w'), ensure_ascii=False)
    for (kind, sp), nv in zip(allS, navs):
        sid = sp['id']
        theme.NAV.clear()
        theme.NAV.update(nv)
        if callable(sp.get('html')):
            sp['html'], sp['html_est'] = sp['html']()
        html_ = render(kind, sp)
        if html_.count('<') > 0 and html_.count('<div') - html_.count('</div>') != 0:
            theme.WARN.append(f'{sid}: unbalanced div')
        n_el = len(re.findall(r'<(div|p|h1|h2|h3|img|table|tr|th|td|x-icon|x-shape|br|b|span)\b', html_))
        if n_el > 195:
            theme.WARN.append(f'{sid}: {n_el} elements')
        open(f'{OUT}/slides/{sid}.html', 'w', encoding='utf-8').write(html_)
    return ids, allS

if __name__ == '__main__':
    mods = sys.argv[1].split(',')
    ids, allS = main(mods)
    print(len(ids), 'slides')
    for w in theme.WARN:
        print('WARN', w)
    json.dump(ids, open('ids.json', 'w'))
    if '-v' in sys.argv:
        print(theme.EST)
