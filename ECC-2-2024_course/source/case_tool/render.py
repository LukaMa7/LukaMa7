# -*- coding: utf-8 -*-
"""Convert generated DOCX/XLSX to PDF with LibreOffice and render PNG pages for visual QA.

Output goes to case_tool/_render/ (never into deliver/). Usage:
    python3 render.py [substring-filter] [--dpi 60]
"""
import glob
import os
import shutil
import subprocess
import sys

from common import OUT, HERE

RENDER = os.path.join(HERE, '_render')


def main():
    flt = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else ''
    dpi = '60'
    if '--dpi' in sys.argv:
        dpi = sys.argv[sys.argv.index('--dpi') + 1]
    files = sorted(glob.glob(os.path.join(OUT, '**', '*.docx'), recursive=True) +
                   glob.glob(os.path.join(OUT, '**', '*.xlsx'), recursive=True))
    files = [f for f in files if flt in f and '05_' not in os.path.relpath(f, OUT)]
    os.makedirs(RENDER, exist_ok=True)
    profile = os.path.join(HERE, '_lo_profile')
    for i, f in enumerate(files):
        rel = os.path.relpath(f, OUT).replace(os.sep, '__')
        stem = os.path.splitext(rel)[0]
        tmpdir = os.path.join(RENDER, 'tmp')
        shutil.rmtree(tmpdir, ignore_errors=True)
        os.makedirs(tmpdir)
        subprocess.run(['soffice', '-env:UserInstallation=file://' + profile, '--headless', '--convert-to', 'pdf',
                        '--outdir', tmpdir, f], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        pdf = glob.glob(os.path.join(tmpdir, '*.pdf'))[0]
        dst = os.path.join(RENDER, stem + '.pdf')
        shutil.move(pdf, dst)
        for old in glob.glob(os.path.join(RENDER, stem + '-*.png')):
            os.remove(old)
        subprocess.run(['pdftoppm', '-r', dpi, '-png', dst, os.path.join(RENDER, stem)], check=True)
        pages = subprocess.run(['pdfinfo', dst], capture_output=True, text=True).stdout
        npages = [l for l in pages.splitlines() if l.startswith('Pages')]
        print(stem, npages[0] if npages else '')
    shutil.rmtree(os.path.join(RENDER, 'tmp'), ignore_errors=True)


if __name__ == '__main__':
    main()
