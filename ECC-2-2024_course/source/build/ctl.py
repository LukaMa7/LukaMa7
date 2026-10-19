import json, re
from corrections import ROWS, NOTES_ADD, NOTES_REPL
X = json.load(open('extracted.json', encoding='utf-8'))
NATIONAL = {'1-2-1', '1-2-2', '2-8-3', '2-13-3-3', '2-13-3-4', '4-1-3-2'}  # Saudi-specific elements (verified); 1-2-3 is governance, 2-12-3-5 is a fixed ECC duration
SPECIAL = {
 '1-1-1': 'توثيق واعتماد', '1-1-2': 'تطبيق', '1-1-3': 'مراجعة دورية',
 '1-2-1': 'متطلب وطني', '1-2-2': 'متطلب وطني', '1-2-3': 'حوكمة',
 '1-3-1': 'توثيق واعتماد', '1-3-2': 'تطبيق', '1-3-3': 'معايير تقنية', '1-3-4': 'مراجعة دورية',
 '1-4-1': 'توثيق واعتماد', '1-4-2': 'مراجعة دورية',
 '1-5-1': 'توثيق واعتماد', '1-5-2': 'تطبيق', '1-5-4': 'مراجعة دورية',
 '1-6-1': 'توثيق واعتماد', '1-6-4': 'مراجعة دورية',
 '1-7-1': 'ضابط شرطي',
 '1-8-1': 'مراجعة داخلية', '1-8-2': 'تدقيق مستقل', '1-8-3': 'عرض النتائج',
 '1-9-1': 'توثيق واعتماد', '1-9-2': 'تطبيق', '1-9-5': 'عند الانتهاء', '1-9-6': 'مراجعة دورية',
 '1-10-1': 'توثيق واعتماد', '1-10-2': 'تطبيق', '1-10-3': 'حد أدنى', '1-10-4': 'تدريب متخصص', '1-10-5': 'مراجعة دورية',
 '2-1-1': 'توثيق واعتماد', '2-1-2': 'تطبيق', '2-1-3': 'توثيق وتعميم', '2-1-4': 'تطبيق', '2-1-5': 'التصنيف', '2-1-6': 'مراجعة دورية',
 '2-7-1': 'توثيق واعتماد', '2-7-2': 'تطبيق', '2-7-3': 'مراجعة دورية',
 '2-8-3': 'حد أدنى · وطني', '2-12-3-5': 'حد أدنى · مدة محددة', '2-9-4': 'مراجعة التطبيق',
 '4-1-1': 'توثيق واعتماد', '4-1-4': 'مراجعة دورية',
}
PREFIX = {'1-6-2': 'بوابة الإطلاق', '1-6-3': 'تطوير البرمجيات', '1-9-3': 'قبل التعيين', '1-9-4': 'أثناء العمل', '1-10-4': 'تدريب متخصص', '1-5-3': 'حالات التقييم',
          '4-1-2': 'بنود العقود', '4-1-3': 'الإسناد والمُدارة'}

def tag(code):
    if code in SPECIAL:
        return SPECIAL[code]
    p = code.split('-')
    base = '-'.join(p[:3])
    if len(p) == 4:
        t_ = PREFIX.get(base, 'حد أدنى')
        return t_ + (' · وطني' if code in NATIONAL else '')
    if len(p) == 3:
        return {'1': 'توثيق واعتماد', '2': 'تطبيق', '4': 'مراجعة دورية'}.get(p[2], '')
    return ''

def R(sid, only=None, drop=()):
    rows = X[sid]['tables'][0][1:]
    out = []
    for r in rows:
        code = r[0]
        if only and code not in only:
            continue
        if code in drop:
            continue
        fix = ROWS.get(code, {})
        out.append((code, fix.get('req', r[1]), fix.get('how', r[2]), fix.get('ev', r[3]), tag(code)))
    return out

def NOTE(sid):
    n = X[sid]['notes']
    for a, b in NOTES_REPL.get(sid, []):
        assert a in n, (sid, a[:40])
        n = n.replace(a, b)
    return n + NOTES_ADD.get(sid, '')

def goal(sid):
    for x in X[sid]['text']:
        m = re.match(r'p: الهدف: ?(.*)', x)
        if m and m.group(1):
            return m.group(1)
    # goal in next line
    tx = X[sid]['text']
    for i, x in enumerate(tx):
        if x.strip() == 'p: الهدف:':
            return tx[i + 1][3:]
    return None
