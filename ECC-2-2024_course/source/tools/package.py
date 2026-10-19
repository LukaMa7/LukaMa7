# Copies the deliverables into the repository folder: deck, original, trainee files, trainer-only files, reports, fonts, source.
# usage: python3 package.py <dest dir>
import os, sys, shutil, glob
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = sys.argv[1]
ATT = os.path.join(SP, 'deliver', 'attachments')
TRAINER = ('الحل_ومعيار_التصحيح', 'مفتاح', 'README_المرفقات')  # file names that stay with the trainer

def cp(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)

if os.path.isdir(DEST):
    shutil.rmtree(DEST)
D = lambda *p: os.path.join(DEST, *p)
cp(os.path.join(SP, 'deliver', 'README.md'), D('README.md'))

# 01 corrected deck
for fn, out in [('ECC-2-2024_course_corrected.pptx', 'ECC-2-2024_course_corrected.pptx'),
                ('ECC-2-2024_course_corrected.pdf', 'ECC-2-2024_course_corrected_معاينة.pdf'),
                ('ECC-2-2024_course_corrected_reference.pdf', 'ECC-2-2024_course_corrected_مرجع_التصميم.pdf')]:
    cp(os.path.join(SP, 'pptx_final', fn), D('01_العرض_المصحح', out))
# 02 original v39, converted with the same tool (content unchanged)
for fn, out in [('ecc_2024_course.pptx', 'ECC-2-2024_course_v39_الأصل.pptx'), ('ecc_2024_course.pdf', 'ECC-2-2024_course_v39_الأصل_معاينة.pdf')]:
    cp(os.path.join(SP, 'pptx_out', fn), D('02_النسخة_الأصلية_v39', out))
# 03 trainee / 04 trainer-only
for f in sorted(glob.glob(os.path.join(ATT, '**', '*.*'), recursive=True)):
    rel = os.path.relpath(f, ATT)
    who = '04_ملفات_المدرب_فقط' if any(k in os.path.basename(f) for k in TRAINER) else '03_ملفات_المتدرب'
    cp(f, D(who, rel))
# 05 reports
for f in sorted(glob.glob(os.path.join(SP, 'deliver', 'reports', '*.*'))):
    cp(f, D('05_التقارير', os.path.basename(f)))
rep = open(os.path.join(SP, 'pptx_final', 'qa', 'report.md'), encoding='utf-8').read()  # file names as delivered, no local paths
rep = rep.replace(os.path.join(SP, 'pptx_final') + os.sep, '').replace('ECC-2-2024_course_corrected.pdf', 'ECC-2-2024_course_corrected_معاينة.pdf')
os.makedirs(D('05_التقارير'), exist_ok=True)
open(D('05_التقارير', 'تقرير_فحص_التحويل_LibreOffice.md'), 'w', encoding='utf-8').write(rep)
# 06 fonts (OFL)
for f in glob.glob(os.path.join(SP, 'pptx_final', 'fonts', '**', '*.*'), recursive=True):
    cp(f, D('06_الخطوط', os.path.relpath(f, os.path.join(SP, 'pptx_final', 'fonts'))))
# source (generators, as used in the working folder)
SRC = [('build', '*.py'), ('build', '*.json'), ('case_tool', '*.py'), ('pptx_tool', '*.py'), ('pptx_tool', '*.cjs'), ('pptx_tool', '*.md'),
       ('pptx_tool/vendor', 'LICENSES.md'), ('qa', 'changes.py'), ('qa', 'extra_sources.json'), ('qa', 'not_done.json'), ('verify', 'source_log.csv')]
for d, pat in SRC:
    for f in glob.glob(os.path.join(SP, d, pat)):
        cp(f, D('source', d, os.path.basename(f)))
for fn in ['make_quiz_docs.py', 'make_reports.py', 'dumptext.py', 'overlap.cjs', 'split_codes.cjs', 'package.py']:
    cp(os.path.join(SP, 'tools', fn), D('source', 'tools', fn))
shutil.copytree(os.path.join(SP, 'deck_new', 'project'), D('source', 'deck_html'))
n = sum(len(fs) for _, _, fs in os.walk(DEST))
print(n, 'files ->', DEST)
