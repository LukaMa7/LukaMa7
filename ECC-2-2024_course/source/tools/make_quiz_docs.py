# Knowledge quiz: trainee question sheet + separate trainer key (same data as the slides: build/c_quiz.QS)
import os, sys
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SP, 'case_tool'))
sys.path.insert(0, os.path.join(SP, 'build'))
os.chdir(os.path.join(SP, 'build'))
from common import RDoc, OUT  # noqa: E402
import common  # course-level files: not entity training data
common.FOOTER = common.MARK = 'الكورس 3 · تطبيق الضوابط الأساسية للأمن السيبراني ECC-2:2024'
common.ENTITY_FULL = 'ملف للكورس'
from c_quiz import QS  # noqa: E402

folder = os.path.join(OUT, '05_الاختبار_المعرفي')
HDR = 'الاختبار النهائي · الجزء الأول: المعرفة · ECC-2:2024'

d = RDoc(HDR, title='أسئلة الاختبار المعرفي')
d.title_block('الاختبار النهائي · الجزء الأول: أسئلة المعرفة', 'عشرة أسئلة اختيار من متعدد · 10 دقائق · كتاب مغلق', 'ورقة المتدرب')
d.p('الاسم: ______________________        التاريخ: ______________')
d.p('اختر إجابة واحدة لكل سؤال واكتب حرفها في المربع. هذا الجزء يقيس المعرفة الأساسية فقط؛ الجزء الثاني (اختبار الأداء) يقيس الحكم على الأدلة، وهو الأهم.', size=10.5)
for n, q, opts, *_ in QS:
    d.p(f'**{n}. {q}**', before=6, keep=True)
    for o in opts:
        d.bullet(o)
    d.p('الإجابة: [   ]', size=10.5)
d.save(os.path.join(folder, 'أسئلة_الاختبار_المعرفي.docx'))

k = RDoc(HDR, trainer_only=True, title='مفتاح الاختبار المعرفي ومعيار التصحيح')
k.title_block('مفتاح الاختبار المعرفي ومعيار التصحيح', 'للمدرب فقط · لا يُعرض قبل تسليم الإجابات', 'ملف منفصل عن الأسئلة')
k.table(['#', 'الإجابة', 'التوضيح', 'المرجع'], [[str(n), a, ex, ref] for n, q, o, a, ex, ref in QS], [1.0, 1.6, 10.4, 4.0], size=10)
k.h('معيار التصحيح', 2)
for line in ['درجة واحدة لكل إجابة صحيحة؛ الحد المقترح للاجتياز في هذا الجزء 7 من 10.',
             'يُحسب هذا الجزء 30% من الدرجة النهائية، واختبار الأداء 70%؛ فلا يكفي حفظ أرقام الضوابط للنجاح.',
             'بعد التصحيح راجع مع المتدربين أي سؤال أخطأ فيه أكثر من ثلثهم، وارجع إلى شريحته.',
             'الأسئلة 1 و4 و9 تقيس متطلبات وطنية وتغييرات مهمة في الإصدار الثاني؛ والسؤال 3 يقيس فهم «بحد أدنى» لا الحفظ.',
             'المرجع الملزم هو النص العربي لوثيقة ECC-2:2024 من موقع الهيئة الوطنية للأمن السيبراني.']:
    k.bullet(line)
k.save(os.path.join(folder, 'مفتاح_الاختبار_المعرفي_للمدرب.docx'))
print('ok', folder)
