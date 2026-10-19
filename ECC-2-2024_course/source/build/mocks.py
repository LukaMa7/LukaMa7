# Illustrative mock evidence (clearly labelled as such on the slide)
from theme import *

MW = 868   # media column width
MH = 540   # media max height

def window(title, body, est, app=None, width=MW):
    dots = ''.join(f'<div style="width:14px;height:14px;border-radius:50%;background:{c}"></div>' for c in ('#E46A5A', '#E8B44A', '#5DB27A'))
    bar = (f'<div style="display:flex;flex-direction:row;align-items:center;gap:10px;background:{INK};padding:12px 20px">{dots}'
           f'<div style="flex:1"></div><p style="font-size:24px;line-height:1.3;color:{ON}">{t(title)}</p></div>')
    h = (f'<div style="display:flex;flex-direction:column;background:#FBFAF7;border:1px solid {LINE};border-radius:16px;overflow:hidden;box-shadow:0 8px 32px rgba(14,26,43,.10)">'
         f'{bar}<div style="display:flex;flex-direction:column;gap:14px;padding:20px 22px">{body}</div></div>')
    return h, est + 56 + 40

def mtable(head, rows, widths, size=24, status_col=None, mono=()):
    """head/rows in reading order; status values colored by keyword"""
    def stc(v):
        tok = v.replace('·', ' ').split()
        if any(k in v for k in ('غير', 'متأخر', 'مفتوح', 'نشط بعد', 'فشل', 'ناقص', 'متوقف', 'مراقبة فقط', 'فجوة', 'حسابات', 'حساباً')) or 'لا' in tok or 'لم' in tok:
            if 'لا فجوة' not in v:
                return '#A6461A'
        if any(k in v for k in ('مطبق', 'متحقق', 'مكتمل', 'في الموعد', 'ناجح', 'معطل', 'مغلق', 'سليم', 'تم', 'معتمد', 'لا فجوة', 'وضع المنع', 'متعدد العوامل')) or 'نعم' in tok:
            return '#22704E'
        return TEXT
    sc = status_col if isinstance(status_col, (tuple, list)) else ((status_col,) if status_col is not None else ())
    hr = ''.join(f'<th style="width:{w}%;text-align:right;color:{TEXT};font-weight:700">{t(h)}</th>' for h, w in reversed(list(zip(head, widths))))
    out = [f'<tr style="background:{PAPER2}">{hr}</tr>']
    for i, r in enumerate(rows):
        tds = []
        for j, c in reversed(list(enumerate(r))):
            st = []
            if j in sc:
                st.append(f'color:{stc(c)};font-weight:600')
            if j in mono:
                st.append(f'font-family:{M}')
            s = f' style="{";".join(st)}"' if st else ''
            tds.append(f'<td{s}>{c if j in mono else t(c)}</td>')
        out.append(f'<tr style="background:{"#FBFAF7" if i % 2 == 0 else "#F3F1EC"}">{"".join(tds)}</tr>')
    est = size * 2.1 * (len(rows) + 1)
    return f'<table style="font-size:{size}px;line-height:1.35;color:{TEXT};border:1px solid {LINE}">{"".join(out)}</table>', est

def terminal(lines_, title='Terminal', size=24):
    ps = []
    for kind, txt in lines_:
        col = {'cmd': '#7FB2EA', 'out': ON, 'ok': '#7CCBA2', 'dim': ON_SOFT, 'warn': '#F29A68'}[kind]
        pre = '$ ' if kind == 'cmd' else ''
        ps.append(f'<p style="font-family:{M};font-size:{size}px;line-height:1.45;color:{col};text-align:left">{esc(pre + txt)}</p>')
    dots = ''.join(f'<div style="width:14px;height:14px;border-radius:50%;background:{c}"></div>' for c in ('#E46A5A', '#E8B44A', '#5DB27A'))
    h = (f'<div style="display:flex;flex-direction:column;background:{INK};border-radius:16px;overflow:hidden">'
         f'<div style="display:flex;flex-direction:row;align-items:center;gap:10px;background:{INK3};padding:12px 20px">{dots}<p style="font-family:{M};font-size:24px;line-height:1.3;color:{ON_SOFT};text-align:left">{esc(title)}</p></div>'
         f'<div style="display:flex;flex-direction:column;gap:6px;padding:22px 26px">{"".join(ps)}</div></div>')
    est = 52 + 44 + sum(lines(x, size, MW - 52, 0.6) * size * 1.45 + 6 for _, x in lines_)
    return h, est

def doc(title, meta, body_items, sign=None, stamp=None):
    """A document page: title, meta rows (label, value), body bullet lines, signature block"""
    mrows = ''.join(f'<div style="display:flex;flex-direction:row-reverse;gap:16px;border-bottom:1px solid {LINE};padding:6px 0">'
                    f'<p style="font-size:24px;font-weight:600;line-height:1.35;color:{SOFT};min-width:170px">{t(a)}</p>'
                    f'<p style="flex:1;font-size:24px;line-height:1.35;color:{TEXT}">{t(b)}</p></div>' for a, b in meta)
    est = 44 + len(meta) * 46
    bl = ''
    for x in body_items:
        bl += f'<div style="display:flex;flex-direction:row-reverse;align-items:center;gap:12px"><div style="width:8px;min-width:8px;height:8px;border-radius:50%;background:{SOFT}"></div><p style="flex:1;font-size:24px;line-height:1.4;color:{TEXT}">{t(x)}</p></div>'
        est += th(x, 24, MW - 120, 1.4) + 8
    sg = ''
    if sign:
        cells = ''.join(f'<div style="flex:1;display:flex;flex-direction:column;gap:4px;border-top:2px solid {TEXT};padding-top:8px">'
                        f'<p style="font-size:24px;font-weight:600;line-height:1.35;color:{TEXT}">{t(a)}</p><p style="font-size:24px;line-height:1.35;color:{MUTED}">{t(b)}</p></div>' for a, b in sign)
        sg = f'<div style="display:flex;flex-direction:row-reverse;gap:36px;padding-top:6px">{cells}</div>'
        est += 90
    st = ''
    if stamp:
        st = f'<p style="font-size:24px;font-weight:700;line-height:1.3;color:#22704E;border:2px solid #22704E;border-radius:10px;padding:4px 14px;align-self:flex-start">{t(stamp)}</p>'
    h = (f'<div style="display:flex;flex-direction:column;gap:12px;background:#FBFAF7;border:1px solid {LINE};border-radius:12px;padding:28px 34px;box-shadow:0 8px 32px rgba(14,26,43,.10)">'
         f'<div style="display:flex;flex-direction:row-reverse;align-items:center;gap:16px"><h3 style="flex:1;font-family:{H};font-size:30px;font-weight:700;line-height:1.35;color:{TEXT}">{t(title)}</h3>{st}</div>'
         f'{mrows}<div style="display:flex;flex-direction:column;gap:8px">{bl}</div>{sg}</div>')
    return h, est + 56 + 48

def kvgrid(pairs, cols=2, label_w=210, size=24, width=1600):
    """label/value pairs laid out in `cols` columns (reading order right to left); height estimated with wrapping"""
    cw = (width - 24 * (cols - 1)) / cols
    cells, hs = [], []
    for k, v in pairs:
        cells.append(f'<div style="display:flex;flex-direction:row-reverse;gap:14px;align-items:flex-start;border-bottom:1px solid {LINE};padding:7px 0">'
                     f'<p style="font-size:{size}px;font-weight:700;line-height:1.4;color:{SOFT};min-width:{label_w}px;width:{label_w}px">{t(k)}</p>'
                     f'<p style="flex:1;font-size:{size}px;line-height:1.4;color:{TEXT}">{t(v)}</p></div>')
        hs.append(max(th(k, size, label_w, 1.4), th(v, size, cw - label_w - 14, 1.4)) + 15)
    rows = math.ceil(len(cells) / cols)
    est = sum(max(hs[i * cols:(i + 1) * cols]) for i in range(rows))
    return f'<div style="display:grid;grid-template-columns:repeat({cols}, 1fr);gap:0 24px">{"".join(rtl_rows(cells, cols))}</div>', est
