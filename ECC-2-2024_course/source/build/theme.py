# Design system + components for the ECC deck (RTL Arabic, 1920x1080 canvas)
import html, math, re

H = "'Alexandria', Tahoma, sans-serif"
B = "'IBM Plex Sans Arabic', Tahoma, sans-serif"
M = "'IBM Plex Mono', 'Courier New', monospace"

INK = '#0E1A2B'; INK2 = '#17273D'; INK3 = '#22344D'
PAPER = '#F5F3EE'; PAPER2 = '#ECE8DF'; CARD = '#FCFBF8'; LINE = '#DDD7CA'
TEXT = '#132033'; SOFT = '#465264'; MUTED = '#5A6371'
ON = '#F2EEE6'; ON_SOFT = '#AEBACB'; ON_LINE = 'rgba(242,238,230,.16)'
WORK = '#E6ECF0'  # exercise background

C = {  # main, tint, light (on dark)
    'base': ('#0B6F7C', '#DCEEEF', '#6CC9D3'),
    'gov':  ('#A6461A', '#F6E6DC', '#F29A68'),
    'def':  ('#1D5B9E', '#E1EAF4', '#7FB2EA'),
    'res':  ('#8A6100', '#F4EAD2', '#E8C35A'),
    'tp':   ('#22704E', '#DFEEE6', '#7CCBA2'),
}
RLE = '&#8235;'
FOOT = 'ECC-2:2024 · تطبيق الضوابط الأساسية للأمن السيبراني'

WARN = []
EST = {}

# navigation state, set by build.py before each slide renders
NAV = {}   # mod, sub (code, name, k, n, stages, kind, idx, cnt), pos
POS = {}   # slide id -> 1-based slide number
MODNAME = {'00': 'المقدمة', '01': 'مفاهيم أساسية', '02': 'أساسيات ECC', '03': 'برنامج التطبيق', '04': 'الحوكمة',
           '05': 'التعزيز (1)', '06': 'التعزيز (2)', '07': 'الصمود والأطراف الخارجية', '08': 'الاستدامة والجاهزية', '09': 'الاختبار والختام'}
MODCOMP = {'00': 'base', '01': 'base', '02': 'base', '03': 'base', '04': 'gov', '05': 'def', '06': 'def', '07': 'tp', '08': 'base', '09': 'base'}
MODITEMS = {}  # unit number -> (module slide id, title, items), filled by build.py
STAGE = {'sub_intro': 'تعريف', 'controls': 'الضوابط', 'evidence': 'الدليل'}

def esc(s):
    s = html.escape(str(s), quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    return s

LRM = '\u200e'
_TOK = re.compile(r'[A-Za-z0-9][A-Za-z0-9.,:/%+\u2013-]*[A-Za-z0-9%]')

def ltr(s):
    """Keep codes, dates and ranges (2-2-3-2, X-4, 2026-08-17, ECC-2:2024, 0\u20133) left-to-right inside Arabic text."""
    return _TOK.sub(lambda m: LRM + m.group(0) + LRM if re.search(r'[-\u2013:/]', m.group(0)) else m.group(0), s)

def t(s):
    """RTL text content."""
    return RLE + ltr(esc(s))

def plain_len(s):
    return len(re.sub(r'\*\*', '', str(s)))

def lines(s, size, width, k=0.5):
    """Greedy wrap estimate (Arabic avg advance ~0.5 em)."""
    words = re.sub(r'\*\*', '', str(s)).split()
    if not words:
        return 0
    cw = size * k; sp = size * 0.28
    n, cur = 1, 0.0
    for w in words:
        ww = len(w) * cw
        if cur == 0:
            cur = ww
        elif cur + sp + ww <= width:
            cur += sp + ww
        else:
            n += 1; cur = ww
        while cur > width:  # very long token
            n += 1; cur -= width
    return n

def th(s, size, width, lh=1.5, k=0.5):
    return lines(s, size, width, k) * size * lh

# ---------------------------------------------------------------- frame
def section(sid, inner, notes, bg=PAPER, color=TEXT, comp='base', foot=None,
            stripe=True, gap=36, justify=None, pad='128px 128px 160px', backdrop='', transition=None, budget_used=None, dark=False):
    st = (f"background:{bg};color:{color};font-family:{B};font-size:28px;line-height:1.5;text-align:right;"
          f"padding:{pad};display:flex;flex-direction:column;gap:{gap}px")
    if justify:
        st += f";justify-content:{justify}"
    tr = f' data-transition="{transition}"' if transition else ''
    out = [f'<section id="{sid}"{tr} style="{st}">']
    if backdrop:
        out.append(backdrop)
    if stripe:
        out.append(f'<div style="position:absolute;left:0;top:0;width:1920px;height:12px;background:{C[comp][0] if not dark else C[comp][2]}"></div>')
    out.append(inner)
    if foot:
        fc = ON_SOFT if dark else MUTED
        out.append(f'<div style="position:absolute;left:128px;bottom:64px;width:1664px;display:flex;flex-direction:row-reverse;align-items:center;gap:24px">'
                   f'<p style="flex:1;font-size:24px;line-height:1.4;color:{fc};text-align:right">{t(foot)}</p>{progress(fc)}</div>')
    if notes:
        n = str(notes).replace('<', '‹').replace('>', '›')
        if len(n) > 3990:
            WARN.append(f'{sid}: notes too long {len(n)}')
            n = n[:3990]
        out.append(f'<aside>{n}</aside>')
    out.append('</section>')
    if budget_used is not None:
        EST[sid] = int(budget_used)
    if budget_used is not None and budget_used > 792:
        WARN.append(f'{sid}: est height {int(budget_used)} > 792')
    return '\n'.join(out)

def header(eyebrow, title, comp='base', crumb=None, dark=False, size=54):
    main, tint, light = C[comp]
    sub = None if dark else NAV.get('sub')
    if sub:
        eyebrow = f'مكوّن فرعي جديد · {sub["k"]} من {sub["n"]}' if sub['kind'] == 'sub_intro' else f'{sub["code"]} · {sub["name"]}'
        crumb = f'الوحدة {NAV["mod"]} · {MODNAME[NAV["mod"]]}'
    if dark:
        pill = f'<p style="font-size:24px;font-weight:600;line-height:1.4;color:{INK};background:{light};padding:6px 20px;border-radius:40px">{t(eyebrow)}</p>'
        cr = f'<p style="font-size:24px;line-height:1.4;color:{ON_SOFT}">{t(crumb)}</p>' if crumb else ''
        tc = ON
    else:
        pill = f'<p style="font-size:24px;font-weight:600;line-height:1.4;color:{main};background:{tint};padding:6px 20px;border-radius:40px">{t(eyebrow)}</p>'
        cr = f'<p style="font-size:24px;line-height:1.4;color:{MUTED}">{t(crumb)}</p>' if crumb else ''
        tc = TEXT
    st = spacer() + stepper(sub, comp) if sub else ''
    h = (f'<div style="display:flex;flex-direction:column;gap:16px">'
         f'<div style="display:flex;flex-direction:row-reverse;align-items:center;gap:18px">{pill}{cr}{st}</div>'
         f'<h2 style="font-family:{H};font-size:{size}px;font-weight:700;line-height:1.3;color:{tc}">{t(title)}</h2></div>')
    est = 46 + 16 + lines(title, size, 1664, 0.56) * size * 1.3
    return h, est

def stepper(sub, comp):
    """Where this slide sits inside its subcomponent: تعريف ← الضوابط ← الدليل"""
    main, tint, light = C[comp]
    out = []
    past = True
    for i, kind in enumerate(sub['stages']):
        now = kind == sub['kind']
        if now:
            past = False
        lab = STAGE[kind]
        if now and sub['cnt'] > 1:
            lab += f' {sub["idx"]} من {sub["cnt"]}'
        if now:
            bg, bd, fg, cbg, mark = main, main, ON, ON, f'<p style="font-family:{H};font-size:24px;font-weight:700;line-height:1;color:{main};text-align:center">{i + 1}</p>'
        elif past:
            bg, bd, fg, cbg, mark = tint, tint, main, main, f'<x-icon name="Check" style="width:20px;height:20px;color:{ON}"></x-icon>'
        else:
            bg, bd, fg, cbg, mark = 'transparent', LINE, MUTED, PAPER2, f'<p style="font-family:{H};font-size:24px;font-weight:700;line-height:1;color:{MUTED};text-align:center">{i + 1}</p>'
        if i:
            out.append(f'<div style="width:20px;height:2px;background:{LINE}"></div>')
        out.append(f'<div style="display:flex;flex-direction:row-reverse;align-items:center;gap:10px;background:{bg};border:1px solid {bd};border-radius:40px;padding:4px 6px 4px 18px">'
                   f'<div style="width:34px;height:34px;border-radius:50%;background:{cbg};display:flex;align-items:center;justify-content:center">{mark}</div>'
                   f'<p style="font-size:24px;font-weight:600;line-height:1.4;color:{fg}">{t(lab)}</p></div>')
    return f'<div style="display:flex;flex-direction:row-reverse;align-items:center;gap:8px">{"".join(out)}</div>'

def progress(fc):
    """Footer: course position across the nine units + slide number"""
    mod = NAV.get('mod')
    if mod is None:
        return ''
    bars = []
    for i in range(1, 10):
        m = f'{i:02d}'
        col = C[MODCOMP[m]][0]
        if m == mod:
            bars.append(f'<div style="width:44px;height:10px;border-radius:5px;background:{col}"></div>')
        elif i < int(mod):
            bars.append(f'<div style="width:22px;height:10px;border-radius:5px;background:{col};opacity:0.4"></div>')
        else:
            bars.append(f'<div style="width:22px;height:10px;border-radius:5px;background:{LINE}"></div>')
    return (f'<div style="display:flex;flex-direction:row-reverse;align-items:center;gap:6px">{"".join(bars)}</div>'
            f'<p style="font-family:{M};font-size:24px;font-weight:600;line-height:1.4;color:{fc};min-width:56px;text-align:left">{NAV["pos"]}</p>')

def icon_chip(name, comp='base', size=64, dark=False, solid=False):
    main, tint, light = C[comp]
    bg = main if solid else (INK3 if dark else tint)
    fg = ON if solid else (light if dark else main)
    return (f'<div style="width:{size}px;height:{size}px;border-radius:16px;background:{bg};display:flex;align-items:center;justify-content:center;align-self:flex-end">'
            f'<x-icon name="{name}" style="width:{int(size*0.56)}px;height:{int(size*0.56)}px;color:{fg}"></x-icon></div>')

def num_badge(n, comp='base', size=52, dark=False):
    main, tint, light = C[comp]
    bg = light if dark else main
    fg = INK if dark else ON
    return (f'<div style="width:{size}px;height:{size}px;min-width:{size}px;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center">'
            f'<p style="font-family:{H};font-size:26px;font-weight:700;line-height:1;color:{fg};text-align:center">{n}</p></div>')

def callout(kind, text, comp='base', label=None, width=1664):
    """Dark band: kind in tip|mistake|note|key"""
    icons = {'tip': 'Lightbulb', 'mistake': 'Warning', 'note': 'Book', 'key': 'Key', 'check': 'CheckCircle', 'lock': 'Lock'}
    labels = {'tip': 'نصيحة عملية', 'mistake': 'خطأ شائع', 'note': 'تذكّر', 'key': 'الفكرة الأساسية', 'check': 'المقيّم يتحقق من', 'lock': 'متطلب وطني'}
    main, tint, light = C[comp]
    lab = label or labels[kind]
    acc = '#F29A68' if kind == 'mistake' else light
    h = (f'<div style="display:flex;flex-direction:row-reverse;align-items:center;gap:24px;background:{INK};border-radius:20px;padding:26px 34px">'
         f'<div style="width:60px;height:60px;min-width:60px;border-radius:14px;background:{INK3};display:flex;align-items:center;justify-content:center"><x-icon name="{icons[kind]}" style="width:34px;height:34px;color:{acc}"></x-icon></div>'
         f'<div style="flex:1;display:flex;flex-direction:column;gap:4px"><p style="font-size:24px;font-weight:700;line-height:1.4;color:{acc}">{t(lab)}</p>'
         f'<p style="font-size:26px;line-height:1.45;color:{ON}">{t(text)}</p></div></div>')
    est = 52 + 34 + th(text, 26, width - 170, 1.45)
    return h, est

def chips(items, comp='base', label=None, size=24, dark=False):
    main, tint, light = C[comp]
    bg = INK3 if dark else CARD
    bd = ON_LINE if dark else LINE
    fg = ON if dark else TEXT
    ps = ''.join(f'<p style="font-size:{size}px;line-height:1.4;color:{fg};background:{bg};border:1px solid {bd};padding:8px 20px;border-radius:40px">{t(x)}</p>' for x in items)
    lab = f'<p style="font-size:24px;font-weight:700;line-height:1.4;color:{light if dark else main}">{t(label)}</p>' if label else ''
    h = f'<div style="display:flex;flex-direction:column;gap:14px">{lab}<div style="display:flex;flex-direction:row-reverse;flex-wrap:wrap;gap:14px">{ps}</div></div>'
    tot = sum(plain_len(x) * size * 0.5 + 40 + 14 for x in items)
    est = (34 + 14 if label else 0) + math.ceil(tot / 1664) * (size * 1.4 + 16 + 14)
    return h, est

def rtl_rows(items, cols):
    rows = [items[i:i + cols] for i in range(0, len(items), cols)]
    out = []
    for r in rows:
        pad = cols - len(r)
        out.extend(['<div></div>'] * pad)
        out.extend(reversed(r))
    return out

def card(title, body, icon=None, comp='base', num=None, dark=False, tsize=32, bsize=26, pad=32, extra='', bg=None, width=500):
    main, tint, light = C[comp]
    cbg = bg or (INK2 if dark else CARD)
    bd = ON_LINE if dark else LINE
    tc = ON if dark else TEXT
    bc = ON_SOFT if dark else SOFT
    top = ''
    if icon:
        top = icon_chip(icon, comp, 60, dark)
    elif num is not None:
        top = f'<div style="display:flex;flex-direction:row-reverse">{num_badge(num, comp, 52, dark)}</div>'
    tt = f'<h3 style="font-family:{H};font-size:{tsize}px;font-weight:600;line-height:1.35;color:{tc}">{t(title)}</h3>' if title else ''
    bb = f'<p style="font-size:{bsize}px;line-height:1.45;color:{bc}">{t(body)}</p>' if body else ''
    h = (f'<div style="display:flex;flex-direction:column;gap:12px;background:{cbg};border:1px solid {bd};border-radius:20px;padding:{pad}px">'
         f'{top}{tt}{bb}{extra}</div>')
    iw = width - 2 * pad
    est = 2 * pad + (60 + 12 if (icon or num is not None) else 0) + (lines(title, tsize, iw, 0.56) * tsize * 1.35 + 12 if title else 0) + (th(body, bsize, iw, 1.45) if body else 0)
    return h, est

def card_grid(cards_spec, cols, comp='base', dark=False, gap=28, **kw):
    w = (1664 - gap * (cols - 1)) / cols
    hs, ests = [], []
    for c in cards_spec:
        c = dict(c)
        h, e = card(c.pop('title', ''), c.pop('body', ''), comp=c.pop('comp', comp), dark=dark, width=w, **{**kw, **c})
        hs.append(h); ests.append(e)
    cells = rtl_rows(hs, cols)
    rows = math.ceil(len(hs) / cols)
    est = sum(max(ests[i * cols:(i + 1) * cols]) for i in range(rows)) + gap * (rows - 1)
    return f'<div style="display:grid;grid-template-columns:repeat({cols}, 1fr);gap:{gap}px">{"".join(cells)}</div>', est

# ---------------------------------------------------------------- controls grid
LAYER = {'doc': 'توثيق واعتماد', 'impl': 'تطبيق', 'min': 'حد أدنى', 'rev': 'مراجعة دورية'}

SPLITS = [(20, 23, 20), (18, 21, 24), (17, 19, 27), (16, 18, 29), (21, 25, 17), (19, 26, 18)]  # ev, how, req (fr)

def controls_grid(rows, comp, size=24):
    """rows: list of (code, req, how, ev[, tag]); column widths chosen per table to minimise its height"""
    main, tint, light = C[comp]
    cw = 150 if max(len(r[0]) for r in rows) < 8 else 178  # code column: 8-character codes (2-10-3-2) need ~125px of mono text
    def heights(split):
        tot = sum(split)
        ws = [(1664 - cw) * f / tot - 40 for f in split]
        h = 54
        for r in rows:
            code, req, how, ev = r[:4]
            tag = r[4] if len(r) > 4 else None
            h += max(th(ev, size, ws[0], 1.45), th(how, size, ws[1], 1.45), th(req, size, ws[2], 1.45, 0.53), 34 + (33 * lines(tag, 24, cw - 40) if tag else 0)) + 33
        return h
    split = min(SPLITS, key=heights)
    cols = [f'{split[0]}fr', f'{split[1]}fr', f'{split[2]}fr', f'{cw}px']  # left->right: ev, how, req, code
    hd = lambda s, c=SOFT: f'<div style="padding:10px 20px;border-bottom:3px solid {main}"><p style="font-size:24px;font-weight:700;line-height:1.4;color:{c}">{t(s)}</p></div>'
    cells = [hd('الدليل', main), hd('كيف تطبقه'), hd('المطلوب'), hd('الضابط')]
    for r in rows:
        code, req, how, ev = r[:4]
        tag = r[4] if len(r) > 4 else None
        cell = lambda inner, bg='transparent': f'<div style="padding:16px 20px;border-bottom:1px solid {LINE};background:{bg}">{inner}</div>'
        tagp = f'<p style="font-size:24px;line-height:1.35;color:{MUTED}">{t(tag)}</p>' if tag else ''
        cells.append(cell(f'<p style="font-size:{size}px;line-height:1.45;color:{TEXT}">{t(ev)}</p>', tint))
        cells.append(cell(f'<p style="font-size:{size}px;line-height:1.45;color:{SOFT}">{t(how)}</p>'))
        cells.append(cell(f'<p style="font-size:{size}px;font-weight:600;line-height:1.45;color:{TEXT}">{t(req)}</p>'))
        cells.append(cell(f'<p style="font-family:{M};font-size:26px;font-weight:600;line-height:1.3;color:{main}">{code}</p>{tagp}'))
    return f'<div style="display:grid;grid-template-columns:{" ".join(cols)};gap:0">{"".join(cells)}</div>', heights(split)

# ---------------------------------------------------------------- generic table
def table(head, rows, widths, size=24, comp='base', first_bold=True, mono_cols=(), zebra=True):
    """head/rows in reading order (right->left); widths in % reading order."""
    main, tint, light = C[comp]
    hr = ''.join(f'<th style="width:{w}%;text-align:right;color:{ON};font-weight:700">{t(h)}</th>' for h, w in reversed(list(zip(head, widths))))
    out = [f'<tr style="background:{INK}">{hr}</tr>']
    est = size * 2.1
    tw = 1664
    for i, r in enumerate(rows):
        bg = CARD if (i % 2 == 0 or not zebra) else PAPER2
        tds = []
        mx = 1
        for j, c in reversed(list(enumerate(r))):
            sty = []
            if j == 0 and first_bold:
                sty.append('font-weight:600')
            if j in mono_cols:
                sty.append(f'font-family:{M};color:{main};font-weight:600')
            s = f' style="{";".join(sty)}"' if sty else ''
            txt = c if j in mono_cols else t(c)
            tds.append(f'<td{s}>{txt}</td>')
            mx = max(mx, lines(c, size, tw * widths[j] / 100 - size * 1.2, 0.52))
        out.append(f'<tr style="background:{bg}">{"".join(tds)}</tr>')
        est += mx * size * 1.45 + size * 0.75
    return (f'<table style="font-size:{size}px;line-height:1.45;color:{TEXT};border:1px solid {LINE}">{"".join(out)}</table>', est)

# ---------------------------------------------------------------- bullets (RTL safe, no ul)
def bullets(items, size=28, comp='base', dark=False, width=1664, gap=16, mark='dot'):
    main, tint, light = C[comp]
    col = light if dark else main
    tc = ON if dark else TEXT
    rows = []
    est = 0
    for i, it in enumerate(items):
        if mark == 'num':
            m = num_badge(i + 1, comp, 44, dark)
        elif mark == 'check':
            m = f'<div style="width:44px;min-width:44px;height:44px;display:flex;align-items:center;justify-content:center"><x-icon name="CheckCircle" style="width:36px;height:36px;color:{col}"></x-icon></div>'
        else:
            m = f'<div style="width:14px;min-width:14px;height:14px;border-radius:50%;background:{col}"></div>'
        rows.append(f'<div style="display:flex;flex-direction:row-reverse;align-items:{"flex-start" if mark != "dot" else "center"};gap:18px">{m}<p style="flex:1;font-size:{size}px;line-height:1.45;color:{tc}">{t(it)}</p></div>')
        est += max(44 if mark != 'dot' else 0, th(it, size, width - 70, 1.45)) + gap
    return f'<div style="display:flex;flex-direction:column;gap:{gap}px">{"".join(rows)}</div>', est - gap

def spacer():
    return '<div style="flex:1"></div>'

def col(inner, flex=1, gap=24, extra=''):
    return f'<div style="flex:{flex};display:flex;flex-direction:column;gap:{gap}px{extra}">{inner}</div>'

def row(*children, gap=40, align='stretch'):
    return f'<div style="display:flex;flex-direction:row-reverse;gap:{gap}px;align-items:{align}">{"".join(children)}</div>'

def para(s, size=28, color=SOFT, weight=None, width=None, family=None, lh=1.5):
    st = f'font-size:{size}px;line-height:{lh};color:{color}'
    if weight:
        st += f';font-weight:{weight}'
    if width:
        st += f';width:{width}px'
    if family:
        st += f';font-family:{family}'
    return f'<p style="{st}">{t(s)}</p>'

def h3(s, size=32, color=TEXT):
    return f'<h3 style="font-family:{H};font-size:{size}px;font-weight:600;line-height:1.35;color:{color}">{t(s)}</h3>'

def label(s, comp='base', dark=False):
    main, tint, light = C[comp]
    return f'<p style="font-size:24px;font-weight:700;line-height:1.4;color:{light if dark else main}">{t(s)}</p>'
