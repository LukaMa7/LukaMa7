# -*- coding: utf-8 -*-
"""Check the VISUAL order of control codes and dates in the rendered PDFs (run render.py first).

For every text line, characters are sorted by their x position (left to right on the page), and the
numeric tokens are compared with what the source documents contain. A code shown reversed
(e.g. 2-1-4 instead of 4-1-2) or a date shown as 30-09-2026 is reported.
"""
import glob
import os
import re

import pdfplumber

from common import HERE, official_codes

RENDER = os.path.join(HERE, '_render')
TOK = re.compile(r'(?<![\d-])\d{1,4}(?:-\d{1,4}){1,3}(?![\d-])')


def visual_lines(page):
    rows = {}
    for c in page.chars:
        rows.setdefault(round(c['top'] / 2), []).append(c)
    for k in sorted(rows):
        cs = sorted(rows[k], key=lambda c: c['x0'])
        out, last = [], None
        for c in cs:
            if last is not None and c['x0'] - last > 1.5:
                out.append(' ')
            out.append(c['text'])
            last = c['x1']
        yield ''.join(out)


def main():
    codes = official_codes()
    bad = 0
    for pdf in sorted(glob.glob(os.path.join(RENDER, '*.pdf'))):
        name = os.path.basename(pdf)
        with pdfplumber.open(pdf) as doc:
            for pno, page in enumerate(doc.pages, 1):
                for line in visual_lines(page):
                    for tok in TOK.findall(line):
                        parts = tok.split('-')
                        if len(parts) == 3 and len(parts[2]) == 4 and len(parts[0]) == 2:
                            print(f'{name} p{pno}: reversed date? {tok}')
                            bad += 1
                        elif all(len(p) <= 2 for p in parts) and tok not in codes:
                            rev = '-'.join(reversed(parts))
                            print(f'{name} p{pno}: code not in official text: {tok} (reversed would be {rev})')
                            bad += 1
    print('visual check:', 'OK' if not bad else f'{bad} suspicious tokens')


if __name__ == '__main__':
    main()
