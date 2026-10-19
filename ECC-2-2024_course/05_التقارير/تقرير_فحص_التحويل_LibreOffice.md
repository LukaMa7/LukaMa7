# PPTX conversion QA report

- PPTX: `ECC-2-2024_course_corrected.pptx`
- PDF (LibreOffice render of the PPTX): `ECC-2-2024_course_corrected_معاينة.pdf`
- Slides: 187

Method: every text box/table cell is drawn in a unique colour in a QA copy of the slide, once by Chromium (reference) and once by LibreOffice from a QA copy of the PPTX; their ink bounding boxes are compared: more lines than the reference, overflow beyond the element box (more than the width slack the converter grants) or beyond the enclosing card/slide, a shifted first line, new overlaps between texts, missing text. Latin/code tokens inside RTL text are looked up in left-to-right order in the glyph positions of the PDF. Non-text objects are checked by eye on the sheets (`qa/sheet-*.jpg`).

## Summary

No slide has overflowing, clipped, extra-wrapped or reversed text.

| # | slide | issues |
|---|---|---|

## Informational (not problems)

Texts that need fewer lines in the PPTX than in the reference (PowerPoint/LibreOffice fits a little more per line, partly because of the width slack; nothing overflows because of it), codes that a line break splits at a hyphen, and codes that the Chromium reference shows reversed while the PPTX shows them left-to-right.

- 001 cover - "ماذا يطلب كل ضابط، وكيف تطبقه خطوة بخطوة، وكيف ي...": renders 43px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 002 audience - "من سينفذ الضوابط التقنية على الأنظمة والشبكات، و...": renders 35px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 006 how-read - "جدول: رمز الضابط، وما يطلبه، وكيف تطبقه، والدليل...": renders 35px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 006 how-read - "عمودا «كيف تطبقه» و«الدليل» ممارسات مقترحة من ال...": renders 34px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 010 f-risk - "احتمال أن يستغل تهديدٌ ثغرةً فيصيب أصلاً، مع حجم...": renders 36px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 021 g-more - "مقياس عالمي من 0 إلى 10 لتصنيف خطورة الثغرات.": renders 32px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 026 ecc-scope - "تلتزم الجهة بكل الضوابط المنطبقة عليها، وبعضها ي...": renders 35px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 051 i1-4 - "مثل فريق كرة قدم: لكل لاعب مركز ومهمة واضحة، وإل...": renders 35px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 053 i1-5 - "تُصرف الميزانية على ما يخيف أكثر لا على ما يضر أ...": renders 35px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 053 i1-5 - "مثل الفحص الطبي الدوري، وقبل أي عملية جراحية: نق...": renders 29px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 055 c1-5b - "طلبات تغيير جوهرية مرفق بها تقييم سابق للموافقة": renders 34px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 055 c1-5b - "عند التخطيط للحصول على خدمات طرف خارجي": renders 33px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 057 i1-6 - "أنظمة تُطلق بثغرات معروفة وإعدادات افتراضية، ثم ...": renders 33px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 058 c1-6a - "بوابة الإطلاق": renders 32px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 058 c1-6a - "بوابة الإطلاق": renders 33px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 061 i1-7 - "مثل شركة طيران تلتزم بأنظمة الطيران الدولية فوق ...": renders 35px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 062 c1-7 - "ضابط شرطي": renders 34px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 062 c1-7 - "السجل عند كل اتفاقية أو التزام جديد": renders 33px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 078 i2-1 - "معرفة كل ما تملكه الجهة من أجهزة وأنظمة وبيانات ...": renders 36px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 079 c2-1a - "تحديد متطلبات إدارة الأصول وتوثيقها واعتمادها": renders 35px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 081 ev-2-1 - "GPL-3.0": wrapped at a separator onto the next line (both pieces read left-to-right)
- 085 ev-2-2a - "استثناءات معتمدة": renders 33px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 087 ev-2-2b - "صور توضيحية من الإنترنت، ليست أدلة صادرة عن جهة ...": renders 33px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 091 ev-2-3 - "عدد الأجهزة في سجل الأصول، مقابل الأجهزة المحمية...": renders 30px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 092 i2-4 - "رسالة تصيد تصل إلى كل الموظفين، أو مهاجم يرسل با...": renders 35px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 094 c2-4b - "تقييم أثر موثق، ثم إلزام التحقق على كل مسار يصل ...": renders 33px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 098 c2-5b - "القائمة المعتمدة، ونتيجة فحص منافذ تطابقها": renders 35px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 102 i2-6 - "حماية الحواسيب المحمولة والجوالات والأجهزة اللوح...": renders 31px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 103 c2-6a - "تقرير الأجهزة المسجلة وحالة امتثالها للسياسة": renders 34px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 103 c2-6a - "مراجعة المتطلبات، ونسب التسجيل والامتثال والتشفي...": renders 35px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 112 ex4 - "بين منطقة المستخدمين ومنطقة الخوادم قاعدة جدار ن...": renders 38px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 122 c2-10b - "اختبار التحديث في بيئة غير إنتاجية، ثم نشره وفق ...": renders 30px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 124 i2-11 - "تقييم مدى فعالية قدرات الدفاع لدى الجهة، بمحاكاة...": renders 35px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 127 ev-2-11 - "GPL-2.0": wrapped at a separator onto the next line (both pieces read left-to-right)
- 128 i2-12 - "المهاجم داخل الشبكة أسابيع دون أن يلاحظه أحد، وح...": renders 29px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 128 i2-12 - "مثل كاميرات المراقبة مع حارس يشاهدها: الكاميرا و...": renders 37px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 142 c2-14d - "المحو الآمن وإعادة الاستخدام والإتلاف المادي: مت...": renders 55px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 149 m6 - "الصمود والأطراف الخارجية والسحابة": renders 97px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 151 c3-1a - "ضمان استمرارية أنظمة وإجراءات الأمن السيبراني": renders 34px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 153 ev-3-1 - "تقرير تمرين التعافي من الكوارث · خدمة البوابة ال...": renders 31px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 155 c4-1a - "البند في العقود، وقائمة جهات الاتصال المحدثة": renders 24px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 161 ev-4-2 - "تقييم قبل الاعتماد": renders 26px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 164 m7 - "كيف يبقى ما بنيناه حياً: حزمة وثائق محدثة، وتقوي...": renders 46px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 173 ex7-ans - "[مدير الهويات] للحصر خلال شهر · [مدير البنية] لل...": renders 30px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 174 case-entity - "11 نظاماً، منها البوابة والتطبيق وERP والموارد ا...": renders 34px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 174 case-entity - "بوابة خدمات إلكترونية وتطبيق للأجهزة الذكية؛ 420...": renders 33px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 175 case-apps - "سجل أصول بأهداف الاستعادة، ومهام النسخ، وسجل نجا...": renders 34px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 175 case-apps - "مقارنة النطاق والنتائج بالأهداف والمتطلبات، وحكم...": renders 34px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 180 perf-e1 - "الدليل E1: لقطة إعداد سياسة التحقق متعدد العوامل...": renders 65px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 185 perf-e5b - "البند 4: موقع التشغيل والمراقبة": renders 33px shorter than the reference (fewer lines: PowerPoint fits more per line)
- 186 next-steps - "مجلدات بالرموز، ومالك لكل ضابط، وتاريخ لكل دليل،...": renders 34px shorter than the reference (fewer lines: PowerPoint fits more per line)
