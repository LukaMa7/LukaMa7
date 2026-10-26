# -*- coding: utf-8 -*-
"""Builds the trainee exercise workbook and the trainer guide (solutions and reasoning) as Word files.

usage: python3 build_wb.py <out dir>
Every exercise lives in exNN.py (scenario, exhibits, tasks, answer sheet, and the trainer solution),
so numbers in the scenario and in the solution come from the same data.
"""
import os, re, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'case_tool'))
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Pt  # noqa: E402
from common import RDoc, shade, _set_child, _RPR_ORDER, _PPR_ORDER, ENTITY_FULL, MARK, official_codes  # noqa: E402
from parts import LEGEND  # noqa: E402
from official import OFF, AUTH  # noqa: E402
from entity import SYSTEMS, P, name  # noqa: E402

EXS = [importlib.import_module(f'ex{i:02d}').EX for i in range(1, 13)]
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), 'deliver', 'workbook')
WB_PATH = os.path.join(OUT, 'كراسة_التمارين_التطبيقية.docx')
TG_PATH = os.path.join(OUT, 'دليل_المدرب_شرح_التمارين_والحلول.docx')
JUDGMENTS = [('مطبق', 'الدليل يثبت ما يطلبه نص الضابط كاملاً للنطاق المعني.'),
             ('مطبق جزئياً', 'جزء من المطلوب مثبت، وجزء غائب أو غير مثبت. اذكر الجزأين.'),
             ('غير مطبق', 'الدليل يثبت أن المطلوب غير موجود أو يتعارض معه.'),
             ('لا يمكن الحكم', 'الأدلة المتاحة لا تكفي لأي حكم. اذكر بدقة ما تحتاجه.')]


def fix_zoom(doc):
    """python-docx's template has <w:zoom> without the required percent attribute (schema error)."""
    z = doc.d.settings.element.find(qn('w:zoom'))
    if z is not None and z.get(qn('w:percent')) is None:
        z.set(qn('w:percent'), '100')


# ------------------------------------------------------------------ blocks
def code_block(doc, lines):
    t = doc.d.add_table(rows=1, cols=1)
    t.style = doc.d.styles['Table Grid']
    doc._tbl_rtl(t, [17.0])
    c = t.cell(0, 0)
    shade(c, 'F2F2F2')
    c.paragraphs[0].text = ''
    for i, line in enumerate(lines):
        par = c.paragraphs[0] if i == 0 else c.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.LEFT
        par.paragraph_format.space_after = Pt(0)
        _set_child(par._p.get_or_add_pPr(), 'bidi', _PPR_ORDER, {'val': '0'})  # command lines read left to right
        r = par.add_run(line)
        rpr = r._r.get_or_add_rPr()
        rf = _set_child(rpr, 'rFonts', _RPR_ORDER)
        for k in ('ascii', 'hAnsi', 'cs'):
            rf.set(qn('w:' + k), 'Courier New')
        r.font.size = Pt(8.5)
    doc.d.add_paragraph().paragraph_format.space_after = Pt(2)


def render(doc, blocks):
    for b in blocks:
        k = b[0]
        if k == 'p':
            o = b[2] if len(b) > 2 else {}
            doc.p(b[1], size=o.get('size', 10.5), color=o.get('color'), bold=o.get('bold', False))
        elif k == 'h':
            doc.h(b[1], b[2]).paragraph_format.keep_with_next = True
        elif k == 'bul':
            for t in b[1]:
                doc.bullet(t, size=10.5)
        elif k == 'note':
            doc.note(b[1], fill=b[2] if len(b) > 2 else 'FFF4E5', size=10)
        elif k == 'kv':
            w = b[2] if len(b) > 2 else (4.0, 13.0)
            assert sum(w) <= 17.05, w
            doc.kv(b[1], widths=w, size=b[3] if len(b) > 3 else 10)
        elif k == 'tbl':
            assert abs(sum(b[3]) - 17.0) < 0.06 or sum(b[3]) < 17.0, (b[1], sum(b[3]))
            assert all(len(r) == len(b[1]) for r in b[2]), b[1]
            doc.table(b[1], b[2], b[3], size=b[4] if len(b) > 4 else 9.5)
        elif k == 'email':
            e = b[1]
            doc.note('\n'.join(['**الموضوع:** ' + e['subj']] + e['body']), fill='F5F7FA', size=10)
        elif k == 'code':
            code_block(doc, b[1])
        elif k == 'blank':
            heads, labels, widths = b[1], b[2], b[3]
            h = b[4] if len(b) > 4 else 1.1
            assert sum(widths) <= 17.05, (heads, sum(widths))
            doc.table(heads, [[l] + [''] * (len(heads) - 1) for l in labels], widths, size=9.5, row_height=h)
        elif k == 'lines':
            doc.kv([(lab, '') for lab, _ in b[1]], widths=(5.0, 12.0), size=10, min_height=[hh for _, hh in b[1]])
        else:
            raise ValueError(k)


def meta_rows(ex, trainer=False):
    rows = [('الوحدة في الكورس', ex['unit']), ('الشريحة في العرض', ex['slide']), ('الأسلوب والوقت', f"{ex['mode']} · {ex['minutes']} دقيقة"),
            ('الضوابط والمفاهيم', ex['controls'])]
    return rows


# ------------------------------------------------------------------ trainee workbook
def workbook():
    d = RDoc('كراسة التمارين التطبيقية · ECC-2:2024', title='كراسة التمارين التطبيقية')
    d.title_block('كراسة التمارين التطبيقية', 'تطبيق الضوابط الأساسية للأمن السيبراني ECC-2:2024 · اثنا عشر تمريناً على جهة واحدة', kicker='للمتدرب')
    d.note('كل الأسماء والأرقام والوثائق في هذه الكراسة بيانات تدريبية افتراضية عن «هيئة المدار للخدمات الرقمية». الأشخاص والشركات خيالية، والنطاقات وعناوين الشبكة للأمثلة فقط. لا يُستخدم أي جزء منها دليلاً حقيقياً.', fill='FDECEC', bold_lead='تنبيه:')

    d.h('كيف تستخدم هذه الكراسة', 1)
    for s in ['كل تمرين يبدأ بدورك في القصة، ثم المستندات التي بين يديك، ثم المطلوب، ثم ورقة إجابة تملؤها في الكراسة نفسها.',
              'التمارين 1 إلى 8 تقابل تمارين العرض بالترقيم نفسه، بسيناريو أكمل ومستندات أكثر. التمارين 9 إلى 12 إضافية، لكل منها موضع مقترح في الكورس.',
              'كل التمارين في جهة واحدة، والأحداث مترابطة: ما تكتشفه في تمرين قد يظهر في آخر. لكن كل تمرين يُحل بمستنداته وحدها.',
              'افتح وثيقة الضوابط الرسمية ECC-2:2024 أثناء الحل. النص العربي هو المعتمد، والصياغات المختصرة في الكراسة للشرح فقط.']:
        d.bullet(s, size=10.5)
    d.h('قواعد العمل', 2)
    for s in ['احكم من المستندات المقدمة فقط. لا تخترع دليلاً، ولا تفترض وجود وثيقة لم تُعرض عليك.',
              'ما تحتاجه ولم تجده اكتبه بوصفه «معلومة ناقصة» بدقة: اسم الوثيقة أو السجل والفترة.',
              'اذكر الدليل الذي بنيت عليه حكمك: رمز المستند (مثل م5-3) والصف أو التاريخ.',
              'لا تنسب إلى الضوابط ما ليس فيها. إن لم تجد نصاً يتناول المسألة فقل ذلك.',
              'الإجراء المقترح يكون محدداً: ماذا، وعلى أي نظام، ومن المالك، ومتى (مدد افتراضية للتخطيط).']:
        d.bullet(s, size=10.5)
    d.h('مقياس الحكم', 2)
    d.table(['الحكم', 'متى تستخدمه'], [list(j) for j in JUDGMENTS], [3.5, 13.5], size=10)

    d.h('خريطة التمارين', 1)
    d.table(['#', 'التمرين', 'الوحدة', 'الشريحة', 'الأسلوب', 'الوقت'],
            [[str(e['n']), e['title'], e['unit'], e['slide'], e['mode'], f"{e['minutes']} د"] for e in EXS], [0.8, 6.0, 3.6, 2.6, 2.4, 1.6], size=9)

    d.h('هيئة المدار في صفحة واحدة', 1)
    d.p('جهة حكومية افتراضية تقدم خدماتها للمواطنين عبر بوابة إلكترونية وتطبيق للأجهزة الذكية. نحو 420 موظفاً و60 متعاقداً. مركز البيانات الرئيسي في الرياض، وموقع تعافٍ من الكوارث في مدينة أخرى داخل المملكة. فترة التقييم في أغلب التمارين: الربع الثالث 2026.', size=10.5)
    d.table(['الرمز', 'النظام', 'الاستضافة', 'الأهمية'], [[s[0], s[1].split(' (')[0], s[3], s[6]] for s in SYSTEMS], [1.6, 7.4, 5.6, 2.4], size=9)
    d.table(['الاسم', 'الدور'], [[P[k][0], P[k][1]] for k in ('ceo', 'csgm', 'grc', 'csops', 'itgm', 'infra', 'iam', 'net', 'backup', 'apps', 'hr', 'proc')], [4.5, 12.5], size=9)

    for ex in EXS:
        d.page_break()
        d.h(f"التمرين {ex['n']}: {ex['title']}", 1)
        d.kv(meta_rows(ex), widths=(3.8, 13.2), size=10)
        d.p('ستتعلم في هذا التمرين أن:', bold=True, size=10.5, keep=True)
        for g in ex['goals']:
            d.bullet(g, size=10.5)
        d.note(ex['role'], fill='EEF2F8', bold_lead='دورك:')
        d.h('الموقف', 2)
        for s in ex['story']:
            d.p(s, size=10.5)
        d.h('المستندات', 2)
        for x in ex['exhibits']:
            d.h(f"{x['code']} · {x['title']}", 3).paragraph_format.keep_with_next = True
            d.p(x['src'], size=9, color='555555', keep=True)
            render(d, x['blocks'])
        d.h('المطلوب', 2)
        for i, t in enumerate(ex['tasks'], 1):
            par = d.p(f'**{i}.** {t}', size=10.5)
            par.paragraph_format.space_after = Pt(4)
        d.h('ورقة الإجابة', 2)
        d.kv([('الاسم', ''), ('التاريخ', '')], widths=(3.0, 14.0), size=10, min_height=0.8)
        render(d, ex['sheet'])
    fix_zoom(d)
    return d.save(WB_PATH)


# ------------------------------------------------------------------ trainer guide
def guide():
    d = RDoc('دليل المدرب: شرح التمارين والحلول · ECC-2:2024', trainer_only=True, title='دليل المدرب: شرح التمارين والحلول')
    d.title_block('دليل المدرب', 'شرح التمارين الاثني عشر: الحل، ولماذا، وكيف تُدار وتُصحح', kicker='للمدرب فقط')
    d.h('كيف تستخدم هذا الدليل', 1)
    for s in ['لكل تمرين: لماذا وُضع، وكيف صُمم السيناريو وما فيه من فخاخ مقصودة، وكيف تديره، والحل النموذجي مع سببه، والنص الرسمي للضوابط، والإجابات البديلة المقبولة، والأخطاء الشائعة، وأسئلة النقاش، ومعيار تصحيح من 100.',
              'السيناريو والمستندات في «كراسة التمارين التطبيقية». هذا الدليل يحيل إليها برموز المستندات (مثل م6-3) ولا يكررها.',
              'الحل النموذجي ليس الإجابة الوحيدة. المعيار يكافئ التبرير من الدليل، ويقبل حكماً مختلفاً إذا كان مبرره صحيحاً.',
              'لا توزع هذا الدليل على المتدربين، ولا تعرض الحل قبل أن يسلّموا إجاباتهم.']:
        d.bullet(s, size=10.5)
    d.h('دليل التسميات', 2)
    d.table(['التسمية', 'المعنى'], [[a, b] for a, b in LEGEND], [3.5, 13.5], size=10)
    d.p(AUTH, size=10)
    d.h('مبادئ إدارة التمارين', 2)
    for s in ['دع المتدربين يحاولون قبل أي شرح؛ الخلاف بينهم يكشف الفهم الخاطئ أسرع من المحاضرة.',
              'اسأل دائماً: «ما الدليل في المستند على ما تقول؟». هذا السؤال وحده يصحح أغلب الأخطاء.',
              'إذا سأل متدرب عن معلومة غير موجودة في المستندات، فلا تخترعها له. اطلب منه أن يكتبها «معلومة ناقصة»؛ هذا جزء من المهارة.',
              'افصل في النقاش بين ثلاثة أشياء: ما ينص عليه الضابط، وما هو ممارسة مقترحة، وما هو قاعدة الجهة الافتراضية.']:
        d.bullet(s, size=10.5)
    d.h('خطة الوقت', 2)
    tot = sum(e['minutes'] for e in EXS)
    d.table(['#', 'التمرين', 'الموضع المقترح في الكورس', 'الوقت'],
            [[str(e['n']), e['title'], e['unit'] + (' · بعد الشريحة ' + e['slide'] if e['slide'][0].isdigit() else ' · ' + e['slide']), f"{e['minutes']} د"] for e in EXS] + [['', 'المجموع', '', f'{tot} د (نحو {tot / 60:.1f} ساعات)']],
            [0.8, 6.4, 7.8, 2.0], size=9)
    d.p('إن ضاق الوقت: التمارين 1 و2 و5 و12 تصلح واجباً منزلياً فردياً، والتمارين 3 و4 و6 و8 أكثر فائدة في القاعة لأنها تعتمد على النقاش.', size=10.5)
    d.h('الروابط بين التمارين', 2)
    d.table(['الرابط', 'أين يظهر'], [
        ['أرقام الحسابات المميزة: 37 حساباً، و22 بإلزام مفعّل، و13 بلا إلزام', 'التمرين 5، والمدخل ح3 في التمرين 6، والتمرين 12، وشرائح الأدلة ولوحة المؤشرات'],
        ['الفرق 240 جهازاً بين سجل الأصول ووحدة الحماية', 'التمرين 5 (م5-2)، ثم تفكيكه في التمرين 9، ثم تصحيحه في التمرين 12'],
        ['الجهاز FIN-LT-117 والخادم FS-02', 'التمرين 9 (ف3 وف5)، والمدخلان ح2 وح4 في التمرين 6'],
        ['الدفعة DSP-2026-06 (96 جهازاً)', 'التمرين 9 (ف1)، ثم التمرين 11'],
        ['قاعدة بيانات الموارد البشرية الصامتة منذ 2026-07-29', 'التمرين 8، والاستثناء EXC-V-2026-07 في التمرين 10، والصف 5 في التمرين 12'],
        ['تطبيق مدار (SYS-02) خارج الفحص واختبار الاختراق', 'التمرين 10؛ وخدمة «الدفع بالتقسيط» فيه موضوع المقترح م3 في التمرين 4'],
        ['ست ثغرات حرجة متأخرة من تسع مفتوحة', 'الملف ح في التمرين 2، والتمرين 10، والتمرين 12']], [8.0, 9.0], size=9)

    for ex in EXS:
        s = ex['sol']
        d.page_break()
        d.h(f"التمرين {ex['n']}: {ex['title']}", 1)
        d.kv(meta_rows(ex), widths=(3.8, 13.2), size=10)
        d.h('لماذا هذا التمرين', 2)
        for t in s['why']:
            d.p(t, size=10.5)
        d.h('كيف صُمم السيناريو', 2)
        for t in s['design']:
            d.bullet(t, size=10.5)
        d.h('إدارة التمرين', 2)
        for t in s['run']:
            d.bullet(t, size=10.5)
        d.h('الحل النموذجي ولماذا', 2)
        render(d, s['answer'])
        if s['official']:
            d.h('النص الرسمي للضوابط المستخدمة', 2)
            for c in s['official']:
                d.p(f'[[متطلب رسمي]] {c}: «{OFF[c]}»', size=10)
        d.h('إجابات بديلة مقبولة', 2)
        for t in s['alt']:
            d.bullet(t, size=10.5)
        d.h('أخطاء شائعة وكيف تعالجها', 2)
        for t in s['mistakes']:
            d.bullet(t, size=10.5)
        d.h('أسئلة للنقاش', 2)
        for t in s['discuss']:
            d.bullet(t, size=10.5)
        d.h('معيار التصحيح (100 درجة)', 2)
        total = sum(p for _, p, _ in s['rubric'])
        assert total == 100, (ex['n'], total)
        d.table(['المعيار', 'الدرجة', 'كيف تُمنح'], [[a, str(p), h] for a, p, h in s['rubric']] + [['المجموع', '100', 'التقدير: 85 فأعلى ممتاز، و70 إلى 84 مجتاز، و50 إلى 69 يحتاج تحسيناً، وأقل من 50 غير مجتاز.']], [5.0, 1.6, 10.4], size=9.5)

    d.page_break()
    d.h('ملحق: الضوابط المستخدمة في التمارين', 1)
    d.p('كل ضابط اقتُبس نصه في هذا الدليل، والتمارين التي يظهر فيها. النص منقول من النسخة العربية الرسمية لـ ECC-2:2024؛ و«…» تعني نصاً محذوفاً من ضابط طويل، والقوس المعقوف يضم العبارة الافتتاحية للبنود الفرعية.', size=10.5)
    used = {}
    for ex in EXS:
        for c in ex['sol']['official']:
            used.setdefault(c, []).append(str(ex['n']))
    key = lambda c: [int(x) for x in c.split('-')]
    d.table(['الضابط', 'التمارين'], [[c, '، '.join(v)] for c, v in sorted(used.items(), key=lambda kv: key(kv[0]))], [4.0, 13.0], size=9.5)
    fix_zoom(d)
    return d.save(TG_PATH)


# ------------------------------------------------------------------ checks
def texts(path):
    from docx import Document
    doc = Document(path)
    out = [p.text for p in doc.paragraphs]
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                out.append(c.text)
    return '\n'.join(out).replace('‎', '')


def checks():
    wb, tg = texts(WB_PATH), texts(TG_PATH)
    codes = official_codes()
    bad = set()
    for txt in (wb, tg):
        for m in re.finditer(r'(?<![\d\-./:A-Za-zم])(\d{1,2}(?:-\d{1,2}){1,3})(?![\d\-])', txt):
            c = m.group(1)
            if any(part.startswith('0') for part in c.split('-')):
                continue  # dates like 06-10
            if c not in codes:
                bad.add(c)
    # solution text must not leak into the workbook: every long answer cell or paragraph checked verbatim
    leaks = []
    for ex in EXS:
        for b in ex['sol']['answer']:
            pieces = []
            if b[0] == 'tbl':
                pieces = [c for r in b[2] for c in r[1:]]  # first column repeats the item labels
            elif b[0] in ('p',):
                pieces = [b[1]]
            elif b[0] == 'bul':
                pieces = b[1]
            elif b[0] == 'kv':
                pieces = [v for _, v in b[1]]
            for s in pieces:
                s = str(s)
                if len(s) > 30 and s.replace('‎', '') in wb:
                    leaks.append((ex['n'], s[:60]))
    print('codes not in ECC-2:2024:', sorted(bad) or 'none')
    print('solution text found in workbook:', leaks or 'none')
    return not bad and not leaks


if __name__ == '__main__':
    print(workbook())
    print(guide())
    ok = checks()
    sys.exit(0 if ok else 1)
