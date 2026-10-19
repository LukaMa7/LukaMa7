# Slide templates
from theme import *
from limits import LIMITS

def _foot(spec):
    return spec.get('foot', FOOT)

# ------------------------------------------------------------- cover
def _cover_title(s):  # keep the code on its own line so it never breaks at its hyphen
    return '<br>'.join(t(x) for x in s.replace(' ECC-', '\nECC-').split('\n'))

def cover(sp):
    sq = []
    cols = [('gov', 10), ('def', 15), ('res', 1), ('tp', 2)]
    seq = []
    for k, n in cols:
        seq += [C[k][2]] * n
    for r in range(4):
        cells = ''.join(f'<div style="flex:1;background:{c};border-radius:8px"></div>' for c in seq[r * 7:(r + 1) * 7])
        sq.append(f'<div style="flex:1;display:flex;flex-direction:row-reverse;gap:12px">{cells}</div>')
    motif = (f'<div style="position:absolute;left:128px;top:300px;width:560px;height:320px;display:flex;flex-direction:column;gap:12px">{"".join(sq)}</div>'
             f'<p style="position:absolute;left:128px;top:650px;width:560px;font-size:24px;line-height:1.5;color:{ON_SOFT}">{t(sp["legend"])}</p>')
    inner = (f'<div style="width:1000px;display:flex;flex-direction:column;gap:28px;align-self:flex-end">'
             f'<p style="font-size:26px;font-weight:600;line-height:1.4;color:{C["gov"][2]};letter-spacing:1px">{t(sp["eyebrow"])}</p>'
             f'<h1 style="font-family:{H};font-size:96px;font-weight:800;line-height:1.2;color:{ON}">{_cover_title(sp["title"])}</h1>'
             f'<p style="font-size:34px;font-weight:500;line-height:1.5;color:{ON}">{t(sp["sub"])}</p>'
             f'<p style="font-size:28px;line-height:1.5;color:{ON_SOFT}">{t(sp["meta"])}</p></div>'
             f'{spacer()}'
             f'<div style="display:flex;flex-direction:row-reverse;gap:16px;align-self:flex-end">'
             + ''.join(f'<p style="font-size:24px;line-height:1.4;color:{ON};background:{INK3};padding:10px 22px;border-radius:40px">{t(x)}</p>' for x in sp['tags'])
             + '</div>')
    return section(sp['id'], motif + inner, sp.get('notes'), bg=INK, color=ON, stripe=False, gap=0,
                   pad='128px', transition='fade')

# ------------------------------------------------------------- module divider
def module(sp):
    comp = sp.get('comp', 'base')
    main, tint, light = C[comp]
    band = f'<div style="position:absolute;right:0;top:0;width:28px;height:1080px;background:{light}"></div>'
    items = sp.get('items', [])
    refs = sp.get('refs') or [None] * len(items)
    it = ''
    if items:
        cells = [f'<div style="display:flex;flex-direction:row-reverse;align-items:baseline;gap:16px;border-top:1px solid {ON_LINE};padding-top:14px">'
                 f'<p style="font-family:{M};font-size:26px;font-weight:600;line-height:1.3;color:{light};min-width:110px;text-align:right">{c}</p>'
                 f'<p style="flex:1;font-size:26px;line-height:1.4;color:{ON}">{t(n)}</p>'
                 + (f'<p style="font-size:24px;line-height:1.4;color:{ON_SOFT}">{t(f"الشريحة {r}")}</p>' if r else '')
                 + '</div>' for (c, n), r in zip(items, refs)]
        ncol = sp.get('cols', 3 if len(items) > 8 else (2 if len(items) > 4 else 1))
        wdt = 1664 if ncol > 1 else 900
        it = f'<div style="display:grid;grid-template-columns:repeat({ncol}, 1fr);gap:16px 48px;width:{wdt}px;align-self:flex-end">{"".join(rtl_rows(cells, ncol))}</div>'
    inner = (f'<div style="display:flex;flex-direction:row-reverse;align-items:flex-end;gap:48px">'
             f'<p style="font-family:{H};font-size:200px;font-weight:800;line-height:1;color:{light}">{sp["num"]}</p>'
             f'<div style="flex:1;display:flex;flex-direction:column;gap:16px;padding-bottom:18px">'
             f'<p style="font-size:26px;font-weight:600;line-height:1.4;color:{light}">{t(sp["eyebrow"])}</p>'
             f'<h1 style="font-family:{H};font-size:80px;font-weight:800;line-height:1.2;color:{ON}">{t(sp["title"])}</h1></div></div>'
             f'<p style="font-size:32px;line-height:1.5;color:{ON_SOFT};width:1300px;align-self:flex-end">{t(sp["desc"])}</p>'
             f'{spacer()}{it}')
    return section(sp['id'], band + course_map(sp['num']) + inner, sp.get('notes'), bg=INK, color=ON, stripe=False, gap=36, pad='128px', transition='fade')

def course_map(num):
    """Pinned strip above a unit divider: the nine units, this one named and lit"""
    cells = []
    for i in range(1, 10):
        m = f'{i:02d}'
        light = C[MODCOMP[m]][2]
        if m == num:
            cells.append(f'<p style="font-size:24px;font-weight:700;line-height:1.4;color:{INK};background:{light};padding:4px 18px;border-radius:40px">{t(f"{m} · {MODNAME[m]}")}</p>')
        elif i < int(num):
            cells.append(f'<p style="font-family:{H};font-size:24px;font-weight:600;line-height:1.4;color:{ON_SOFT};background:{INK3};padding:4px 14px;border-radius:40px">{m}</p>')
        else:
            cells.append(f'<p style="font-family:{H};font-size:24px;font-weight:600;line-height:1.4;color:{ON_SOFT};border:1px solid {ON_LINE};padding:4px 14px;border-radius:40px">{m}</p>')
    return (f'<div style="position:absolute;left:128px;top:44px;width:1664px;display:flex;flex-direction:row-reverse;align-items:center;gap:10px">'
            f'<p style="font-size:24px;line-height:1.4;color:{ON_SOFT}">{t("خريطة الكورس")}</p>{"".join(cells)}</div>')

# ------------------------------------------------------------- concept / cards
def concept(sp):
    comp = sp.get('comp', 'base')
    hd, est = header(sp['eyebrow'], sp['title'], comp, sp.get('crumb'))
    parts = [hd]
    gap = sp.get('gap', 36)
    if sp.get('lead'):
        parts.append(para(sp['lead'], 30, SOFT, width=sp.get('lead_w', 1500)))
        est += gap + th(sp['lead'], 30, sp.get('lead_w', 1500))
    if sp.get('cards'):
        g, e = card_grid(sp['cards'], sp.get('cols', 3), comp, **sp.get('card_kw', {}))
        parts.append(g); est += gap + e
    if sp.get('html'):
        parts.append(sp['html']); est += gap + sp.get('html_est', 0)
    if sp.get('callout'):
        k, txt = sp['callout'][:2]
        lab = sp['callout'][2] if len(sp['callout']) > 2 else None
        parts.append(spacer())
        h, e = callout(k, txt, comp, lab); parts.append(h); est += gap + e
    return section(sp['id'], ''.join(parts), sp.get('notes'), comp=comp, foot=_foot(sp), gap=gap, budget_used=est)

# ------------------------------------------------------------- subcomponent intro
def sub_intro(sp):
    comp = sp['comp']
    main, tint, light = C[comp]
    hd, est = header(sp['eyebrow'], f'{sp["code"]}  {sp["name"]}', comp, sp.get('crumb'))
    goal = (f'<div style="display:flex;flex-direction:row-reverse;gap:20px;align-items:flex-start;background:{CARD};border:1px solid {LINE};border-radius:20px;padding:22px 30px">'
            f'<p style="font-size:24px;font-weight:700;line-height:1.5;color:{main};min-width:150px">{t("هدف الوثيقة")}</p>'
            f'<p style="flex:1;font-size:27px;line-height:1.5;color:{TEXT}">{t(sp["goal"])}</p></div>')
    est += 36 + 44 + th(sp['goal'], 27, 1400)
    cs = [dict(title='ببساطة', body=sp['simple'], icon='Lightbulb'),
          dict(title='مثال من الحياة', body=sp['analogy'], icon='Home'),
          dict(title='ماذا لو غاب؟', body=sp['risk'], icon='Warning')]
    g, e = card_grid(cs, 3, comp, tsize=30, bsize=26, pad=30)
    est += 36 + e
    parts = [hd, goal, g]
    if sp.get('terms'):
        terms = ''.join(f'<div style="flex:1;display:flex;flex-direction:column;gap:4px;border-top:3px solid {main};padding-top:14px">'
                        f'<p style="font-size:24px;font-weight:700;line-height:1.4;color:{TEXT}">{t(a)}</p>'
                        f'<p style="font-size:24px;line-height:1.4;color:{SOFT}">{t(b)}</p></div>' for a, b in sp['terms'])
        n = len(sp['terms'])
        w = (1664 - 32 * (n - 1)) / n
        parts.append(spacer())
        parts.append(f'<div style="display:flex;flex-direction:row-reverse;gap:32px">{terms}</div>')
        est += 36 + 14 + 34 + max(th(b, 24, w, 1.4) for a, b in sp['terms'])
    return section(sp['id'], ''.join(parts), sp.get('notes'), bg=tint, comp=comp, foot=_foot(sp), gap=36, budget_used=est)

# ------------------------------------------------------------- controls
def controls(sp):
    comp = sp['comp']
    hd, est = header(sp['eyebrow'], sp['title'], comp, sp.get('crumb'))
    g, e = controls_grid(sp['rows'], comp)
    parts = [hd, g]; est += 32 + e
    if sp.get('steps'):
        parts.append(sp['steps'][0]); est += 32 + sp['steps'][1]
    for ex in sp.get('extras', []):
        if ex[0] == 'chips':
            h, e2 = chips(ex[2], comp, ex[1])
        else:
            h, e2 = callout(ex[0], ex[1], comp, ex[2] if len(ex) > 2 else None)
        parts.append(spacer()); parts.append(h); est += 32 + e2
    return section(sp['id'], ''.join(parts), sp.get('notes'), comp=comp, foot=_foot(sp), gap=32, budget_used=est)

# ------------------------------------------------------------- evidence example
def evidence(sp, media_html, media_est, credit):
    """Evidence example: what kind of material it is, what you see, what the assessor checks, and what it does not prove"""
    comp = sp['comp']
    main, tint, light = C[comp]
    title = sp['title']
    if sp['media']['type'] in ('img', 'img2') and title.startswith('كيف يبدو الدليل: '):
        title = 'مثال توضيحي: ' + title[len('كيف يبدو الدليل: '):]
    hd, est = header(sp['eyebrow'], title, comp, sp.get('crumb'))
    mat = sp.get('material') or ('صورة توضيحية' if sp['media']['type'] in ('img', 'img2') else 'نموذج دليل تدريبي')
    codes = ''.join(f'<p style="font-family:{M};font-size:24px;font-weight:600;line-height:1.3;color:{main};background:{tint};padding:6px 14px;border-radius:12px">{c}</p>' for c in sp['codes'])
    top = (f'<div style="display:flex;flex-direction:row-reverse;flex-wrap:wrap;gap:10px;align-items:center">'
           f'<p style="font-size:24px;font-weight:700;line-height:1.3;color:{ON};background:{INK};padding:6px 16px;border-radius:12px">{t(mat)}</p>'
           f'<p style="font-size:24px;line-height:1.3;color:{MUTED}">{t("يرتبط بالضوابط:")}</p>{codes}</div>')
    lim = sp.get('limits') or LIMITS.get(sp['id'])
    limbox = (f'<div style="display:flex;flex-direction:row-reverse;gap:14px;align-items:flex-start;background:{PAPER2};border-radius:14px;padding:14px 18px">'
              f'<x-icon name="Warning" style="width:30px;height:30px;color:{C["gov"][0]}"></x-icon>'
              f'<p style="flex:1;font-size:24px;line-height:1.45;color:{TEXT}"><b>{t("لا يثبت وحده: ")}</b>{t(lim)}</p></div>') if lim else ''
    if sp.get('wide'):
        cards = ''.join(f'<div style="flex:1;display:flex;flex-direction:row-reverse;gap:14px;align-items:flex-start">{num_badge(i + 1, comp, 40)}'
                        f'<p style="flex:1;font-size:24px;line-height:1.45;color:{TEXT}">{t(p)}</p></div>' for i, p in enumerate(sp['see']))
        mock = sp['media']['type'] == 'mock'  # the badge already says it is a training model
        cred = '' if mock else f'<p style="font-size:24px;line-height:1.4;color:{MUTED}">{t(credit)}</p>'
        strip = ''
        if sp['see']:
            w = (1664 - 2 * 28) / len(sp['see']) - 54
            strip = f'{spacer()}<div style="display:flex;flex-direction:row-reverse;gap:28px;border-top:1px solid {LINE};padding-top:16px">{cards}</div>'
            est += 20 + 17 + max(40, max(th(p, 24, w, 1.45) for p in sp['see']))
        body = f'{top}<div style="display:flex;flex-direction:column;gap:12px">{media_html}{cred}</div>{strip}'
        est += 20 + 44 + 20 + media_est + (0 if mock else 12 + 34)
        return section(sp['id'], hd + body, sp.get('notes'), comp=comp, foot=_foot(sp), gap=20, budget_used=est)
    rw = sp.get('rw', 740)  # width of the text column
    pts = ''
    pe = 0
    for i, p in enumerate(sp['see']):
        pts += (f'<div style="display:flex;flex-direction:row-reverse;gap:16px;align-items:flex-start">{num_badge(i + 1, comp, 40)}'
                f'<p style="flex:1;font-size:24px;line-height:1.45;color:{TEXT}">{t(p)}</p></div>')
        pe += max(40, th(p, 24, rw - 70, 1.45)) + 10
    chk = ''
    ce = 0
    for c in sp['check']:
        chk += (f'<div style="display:flex;flex-direction:row-reverse;gap:14px;align-items:flex-start">'
                f'<div style="width:40px;min-width:40px;height:40px;display:flex;align-items:center;justify-content:center"><x-icon name="CheckCircle" style="width:32px;height:32px;color:{main}"></x-icon></div>'
                f'<p style="flex:1;font-size:24px;line-height:1.45;color:{SOFT}">{t(c)}</p></div>')
        ce += max(40, th(c, 24, rw - 70, 1.45)) + 8
    rightc = (f'<div style="width:{rw}px;display:flex;flex-direction:column;gap:14px">{top}'
              f'{label("ما الذي تراه", comp)}<div style="display:flex;flex-direction:column;gap:10px">{pts}</div>'
              f'<div style="border-top:1px solid {LINE};padding-top:14px;display:flex;flex-direction:column;gap:8px">{label("ما الذي يبحث عنه المقيّم", comp)}{chk}</div>'
              f'{spacer()}{limbox}</div>')
    le_ = (28 + th(lim, 24, rw - 140, 1.45)) if lim else 0
    re_ = 44 + 14 + 34 + 14 + pe - 10 + 14 + 15 + 34 + 8 + ce - 8 + 14 + le_
    leftc = (f'<div style="flex:1;display:flex;flex-direction:column;gap:14px">{media_html}'
             f'<p style="font-size:24px;line-height:1.4;color:{MUTED}">{t(credit)}</p></div>')
    le = media_est + 14 + th(credit, 24, 1664 - 48 - rw, 1.4)
    body = f'<div style="flex:1;display:flex;flex-direction:row-reverse;gap:48px">{rightc}{leftc}</div>'
    est += 32 + max(re_, le)
    return section(sp['id'], hd + body, sp.get('notes'), comp=comp, foot=_foot(sp), gap=32, budget_used=est)

# ------------------------------------------------------------- evidence analysis (reading one piece of evidence)
def judge(sp):
    """Four quadrants: what it proves / what it does not / missing information / judgment and next step"""
    comp = sp['comp']
    main, tint, light = C[comp]
    hd, est = header(sp['eyebrow'], sp['title'], comp, sp.get('crumb'))
    quads = [('ما يثبته الدليل', 'CheckCircle', sp['proves']), ('ما لا يثبته وحده', 'Warning', sp['not']),
             ('المعلومات الناقصة التي تُطلب', 'Search', sp['ask']), ('الحكم والخطوة التالية', 'Key', sp['next'])]
    cells, ests = [], []
    w = (1664 - 28) / 2 - 64
    for ttl, ic, items in quads:
        b, e = bullets(items, 24, comp, width=w, gap=10)
        cells.append(f'<div style="display:flex;flex-direction:column;gap:14px;background:{CARD};border:1px solid {LINE};border-radius:18px;padding:22px 28px">'
                     f'<div style="display:flex;flex-direction:row-reverse;align-items:center;gap:14px">{icon_chip(ic, comp, 48)}'
                     f'<h3 style="font-family:{H};font-size:28px;font-weight:600;line-height:1.3;color:{TEXT}">{t(ttl)}</h3></div>{b}</div>')
        ests.append(44 + 48 + 14 + e)
    grid = f'<div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:24px 28px">{"".join(rtl_rows(cells, 2))}</div>'
    est += 28 + max(ests[0], ests[1]) + 24 + max(ests[2], ests[3])
    parts = [hd, grid]
    if sp.get('callout'):
        h, e = callout(sp['callout'][0], sp['callout'][1], comp, sp['callout'][2] if len(sp['callout']) > 2 else None)
        parts += [spacer(), h]; est += 28 + e
    return section(sp['id'], ''.join(parts), sp.get('notes'), comp=comp, foot=_foot(sp), gap=28, budget_used=est)

# ------------------------------------------------------------- glossary
def glossary(sp):
    comp = sp.get('comp', 'base')
    main, tint, light = C[comp]
    hd, est = header(sp['eyebrow'], sp['title'], comp, sp.get('crumb'))
    cells = []
    ests = []
    w = (1664 - 2 * 28) / 3 - 60
    for ar, en, d in sp['terms']:
        cells.append(f'<div style="display:flex;flex-direction:column;gap:6px;background:{CARD};border:1px solid {LINE};border-radius:20px;padding:28px 30px">'
                     f'<div style="display:flex;flex-direction:row-reverse;align-items:baseline;justify-content:space-between;gap:12px">'
                     f'<h3 style="font-family:{H};font-size:30px;font-weight:600;line-height:1.35;color:{TEXT}">{t(ar)}</h3>'
                     f'<p style="font-family:{M};font-size:24px;font-weight:600;line-height:1.35;color:{main}">{esc(en)}</p></div>'
                     f'<p style="font-size:25px;line-height:1.45;color:{SOFT}">{t(d)}</p></div>')
        ests.append(56 + 41 + 6 + th(d, 25, w, 1.45))
    grid = f'<div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:28px">{"".join(rtl_rows(cells, 3))}</div>'
    rows = (len(cells) + 2) // 3
    est += 36 + sum(max(ests[i * 3:(i + 1) * 3]) for i in range(rows)) + 28 * (rows - 1)
    return section(sp['id'], hd + grid, sp.get('notes'), comp=comp, foot=_foot(sp), gap=36, budget_used=est)

# ------------------------------------------------------------- table page
def tablepage(sp, bg=PAPER, badge=None):
    comp = sp.get('comp', 'base')
    hd, est = header(sp['eyebrow'], sp['title'], comp, sp.get('crumb'))
    parts = [hd]
    if sp.get('lead'):
        parts.append(para(sp['lead'], 28, SOFT, width=1500)); est += 32 + th(sp['lead'], 28, 1500)
    tb, e = table(sp['head'], sp['rows'], sp['widths'], sp.get('size', 24), comp, sp.get('first_bold', True), sp.get('mono', ()))
    parts.append(tb); est += 32 + e
    if sp.get('callout'):
        k, txt = sp['callout'][:2]
        h, e2 = callout(k, txt, comp, sp['callout'][2] if len(sp['callout']) > 2 else None)
        parts.append(spacer()); parts.append(h); est += 32 + e2
    return section(sp['id'], ''.join(parts), sp.get('notes'), bg=bg, comp=comp, foot=_foot(sp), gap=32, budget_used=est)

# ------------------------------------------------------------- exercise
def exercise(sp):
    comp = sp.get('comp', 'base')
    main, tint, light = C[comp]
    hd, est = header(sp['eyebrow'], sp['title'], comp, sp.get('crumb'))
    task = (f'<div style="display:flex;flex-direction:row-reverse;gap:22px;align-items:center;background:{CARD};border:1px solid {LINE};border-radius:20px;padding:24px 32px">'
            f'{icon_chip("Tool", comp, 60)}<p style="flex:1;font-size:28px;line-height:1.45;color:{TEXT}">{t(sp["task"])}</p></div>')
    est += 32 + 48 + max(60, th(sp['task'], 28, 1450, 1.45))
    cols = sp.get('cols', 2)
    w = (1664 - 24 * (cols - 1)) / cols
    items = []
    ie = []
    for i, it in enumerate(sp['items']):
        lab = sp.get('labels', None)
        n = lab[i] if lab else str(i + 1)
        items.append(f'<div style="display:flex;flex-direction:row-reverse;gap:20px;align-items:center;background:{CARD};border:1px solid {LINE};border-radius:18px;padding:20px 26px">'
                     f'{num_badge(n, comp, 50)}<p style="flex:1;font-size:26px;line-height:1.45;color:{TEXT}">{t(it)}</p></div>')
        ie.append(40 + max(50, th(it, 26, w - 120, 1.45)))
    rows = math.ceil(len(items) / cols)
    grid = f'<div style="display:grid;grid-template-columns:repeat({cols}, 1fr);gap:20px 24px">{"".join(rtl_rows(items, cols))}</div>'
    est += 32 + sum(max(ie[i * cols:(i + 1) * cols]) for i in range(rows)) + 20 * (rows - 1)
    return section(sp['id'], hd + task + grid, sp.get('notes'), bg=WORK, comp=comp, foot=_foot(sp), gap=32, budget_used=est)

# ------------------------------------------------------------- statement
def statement(sp):
    comp = sp.get('comp', 'gov')
    main = C[comp][0]
    inner = (f'<p style="font-size:28px;font-weight:600;line-height:1.4;color:{ON};opacity:0.85">{t(sp["eyebrow"])}</p>'
             f'<h1 style="font-family:{H};font-size:76px;font-weight:700;line-height:1.3;color:{ON};width:1500px">{t(sp["text"])}</h1>'
             + (f'<p style="font-size:32px;line-height:1.5;color:{ON};width:1300px;opacity:0.9">{t(sp["sub"])}</p>' if sp.get('sub') else ''))
    return section(sp['id'], inner, sp.get('notes'), bg=main, color=ON, stripe=False, gap=36, justify='center', pad='128px')

# ------------------------------------------------------------- steps (horizontal process)
def steps(items, comp='base', size=26, title_size=30):
    """items: list of (title, body) in reading order; arrows between"""
    main, tint, light = C[comp]
    n = len(items)
    w = (1664 - (n - 1) * 56) / n
    out = []
    ests = []
    for i, (tt, bb) in enumerate(items):
        out.append(f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:{CARD};border:1px solid {LINE};border-top:6px solid {main};border-radius:16px;padding:26px">'
                   f'<p style="font-family:{H};font-size:28px;font-weight:700;line-height:1.2;color:{main}">{i + 1:02d}</p>'
                   f'<h3 style="font-family:{H};font-size:{title_size}px;font-weight:600;line-height:1.35;color:{TEXT}">{t(tt)}</h3>'
                   f'<p style="font-size:{size}px;line-height:1.45;color:{SOFT}">{t(bb)}</p></div>')
        ests.append(52 + 34 + 12 + lines(tt, title_size, w - 52, 0.56) * title_size * 1.35 + 12 + th(bb, size, w - 52, 1.45))
        if i < n - 1:
            out.append(f'<div style="width:32px;display:flex;align-items:center;justify-content:center"><x-shape kind="arrow-left" style="width:32px;height:20px;background:{main}"></x-shape></div>')
    return f'<div style="display:flex;flex-direction:row-reverse;gap:12px">{"".join(out)}</div>', max(ests)

# ------------------------------------------------------------- performance test exhibit (no hints: no control codes, no analysis)
def exhibit(sp):
    comp = sp.get('comp', 'base')
    main, tint, light = C[comp]
    hd, est = header(sp['eyebrow'], sp['title'], comp, sp.get('crumb'))
    top = (f'<div style="display:flex;flex-direction:row-reverse;align-items:center;gap:14px">'
           f'<p style="font-size:24px;font-weight:700;line-height:1.3;color:{ON};background:{INK};padding:6px 16px;border-radius:12px">{t("دليل اختبار · بيانات افتراضية")}</p>'
           f'<p style="flex:1;font-size:24px;line-height:1.4;color:{SOFT}">{t(sp.get("ask", "أجب في ورقة الإجابة: الضابط، وما يثبته، وما لا يثبته، والناقص، والحكم ومبرره، والخطوة التالية."))}</p></div>')
    mh, me = sp['media']['fn']()
    body = f'{top}{mh}'
    est += 24 + 44 + 24 + me
    return section(sp['id'], hd + body, sp.get('notes'), bg=WORK, comp=comp, foot=_foot(sp), gap=24, budget_used=est)
