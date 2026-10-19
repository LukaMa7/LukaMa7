# HTML slide deck → editable PowerPoint

Converts an Arabic (RTL) HTML deck — `deck.json` + `slides/<id>.html`, one `<section>` per slide on a
1920×1080 canvas, inline styles only — into an **editable** `.pptx`: native text boxes, shapes, tables,
pictures and speaker notes (never a screenshot per slide). It also writes a LibreOffice PDF of the PPTX,
a reference PDF straight from Chromium, reference PNGs and side-by-side QA sheets with an automatic report.

## Usage

```bash
python3 -I pptx_tool/build_pptx.py \
    --deck  <project dir with deck.json and slides/> \
    --blobs <blob_map.json: blob id -> local image file> \
    --out   <out dir>/<name>.pptx
```

Options: `--slides id1,id2` (subset, for quick checks), `--no-qa` (PPTX only), `--no-ref-pdf`,
`--keep-work` (keep `<out dir>/_work`), `--reuse-render` (with a kept `_work`: skip Chromium, rebuild only).
A full run of 174 slides takes about 5 minutes.

Requirements: Python 3 with `python-pptx`, `Pillow`, `numpy`, `lxml`, `pdfplumber`; Node with the global
`playwright` package and its Chromium (`PLAYWRIGHT_BROWSERS_PATH`, defaults to `/opt/pw-browsers`);
LibreOffice (`soffice`), poppler (`pdftoppm`), `fc-cache`, `curl`. Fonts and icons are downloaded on the
first run into `pptx_tool/vendor/` (see `vendor/LICENSES.md`); run with `python3 -I` because the tool reads
those downloaded files.

## Outputs (next to `--out`)

| path | what |
|---|---|
| `<name>.pptx` | the editable deck (16:9, 13.333 × 7.5 in, title from `deck.json`, notes from `<aside>`) |
| `<name>.pdf` | the PPTX rendered by LibreOffice (what the QA checks) |
| `<name>_reference.pdf` | all slides printed by Chromium, 1920×1080 pages |
| `ref/<nnn>-<id>.png` | Chromium reference render of each slide |
| `qa/pptx_png/<nnn>-<id>.png` | LibreOffice render of each PPTX slide (960 px wide) |
| `qa/sheet-NN.jpg` | 6 pairs per sheet: reference (left) vs PPTX render (right) |
| `qa/pairs/<nnn>-<id>.jpg` | the same pair for one slide, larger |
| `qa/report.md` | automatic findings (see QA) |
| `fonts/` | the TTFs used + their `OFL.txt` — install them on the machine that opens the PPTX |

## How it works

1. **Fonts** — Alexandria (variable), IBM Plex Sans Arabic 400/500/600/700, IBM Plex Mono 400/600 are
   downloaded from github.com/google/fonts, installed to `~/.local/share/fonts/deck-fonts` (+ `fc-cache`)
   so LibreOffice finds them, and copied to `<out>/fonts/` with their OFL licences.
2. **Render** (`render.cjs`, Playwright/Chromium) — each section is put in a wrapper page that emulates the
   slide host: 1920×1080 `position:relative` section, a `div` without `display` is a flex column, h1–h3 tag
   defaults, tables `width:100%` with collapsed borders, every cell ruled in the table's border colour and
   padded `0.35em 0.6em`, `<aside>` hidden, fonts from `@font-face` on the local TTFs. `x-icon` becomes the
   Phosphor SVG tinted with `currentColor`; `x-shape` becomes an SVG (arrow head = 40 % of the length).
   The page is screenshotted (`ref/`), then the DOM is walked (`getBoundingClientRect` +
   `getComputedStyle`) into paint items in DOM order. Finally every text is repainted in a unique "QA colour"
   on white for the overflow check, icons are rasterized at 4× with a transparent background and the
   reference PDF is printed.
3. **Build** (`build_pptx.py`, python-pptx; 1 px = 6350 EMU, font px × 0.5 = pt)
   - painted `div` → rectangle / rounded rectangle / oval / top- or bottom-rounded rectangle (corners
     clipped by an `overflow:hidden` rounded parent take its radius), fill colour + alpha (rgba × opacity),
     outline for uniform borders, thin filled rectangles for single-side borders (rules). `box-shadow` is ignored.
   - `p`/`h1`–`h3` → one text box at the element box, padding → insets, one paragraph with runs
     (bold for `<b>`/weight ≥ 600, colour, size, italic, letter-spacing; latin + ea + cs typefaces).
     A text element with its own fill/border (pill, badge) becomes that shape with the text inside it;
     the preset's own text rectangle (rounded corners) is compensated in the insets, and the text is centred
     when it fills the box. Word wrap on, autofit off. Line spacing = computed `line-height` (exact points).
   - Text containing Arabic (or starting with U+202B) → `rtl="1"`, alignment as computed. U+202B is
     stripped; any LRM already in the source is kept; an LRM is added before and after every Latin/numeric
     token containing `-`, `:` or `/` (codes `2-2-3-2`, dates `2026-08-17`, `ECC-2:2024`, `X-4`) unless it
     is already there. Without it the bidi algorithm turns digits after Arabic letters into Arabic numbers
     and `2-9-1` displays as `1-9-2`.
   - Width slack: the frame grows on the side opposite the alignment (3 % / ≥ 0.25 em for multi-line text,
     8 % / ≥ 0.6 em for single-line labels, eating padding first, never past the enclosing card or slide),
     so PowerPoint's slightly different line breaking does not add lines or break a word.
   - Vertical calibration: CSS puts a line's baseline at `L/2 + (ascent − descent)/2·fs` (font metrics read
     from the TTFs); LibreOffice with exact spacing puts it at `L − 0.21·fs` (measured; centred table cells use
     the font's Windows metrics instead). Each frame is shifted by the difference (± a few px).
   - `<table>` → native table, column widths/row heights from the rendered cells (visual left-to-right
     order, so the RTL tables written in visual order keep their geometry), row backgrounds as cell fills,
     padding as cell margins, 1 px borders in the table's border colour, "No Style, No Grid" table style.
   - `<img>` → picture; `object-fit:contain` draws the fitted rectangle, `cover` crops
     (`crop_left/right/top/bottom`), rounded corners kept as a `roundRect` picture geometry.
   - `x-icon` → 4× PNG picture at the icon box; `x-shape` → native arrow/oval/diamond autoshape.
   - Slide background = section background; `<aside>` → notes; `hidden` → hidden slide;
     `data-transition` (how a slide leaves) → fade/push transition on the next slide.
4. **QA** — LibreOffice converts the PPTX and a QA copy of it (only the texts, each in its QA colour) to
   PDF; `pdftoppm` renders them. For every text box / table cell the ink bounding box in Chromium's QA
   render is compared with LibreOffice's: more lines than the reference, overflow beyond the element box
   (beyond the granted slack) or beyond its card/slide, a shifted first line, new overlaps between texts,
   missing text. Latin/code tokens of RTL texts are looked up in the glyph x-order of the PDF
   (`pdfplumber`) to prove they read left-to-right; tokens that a line break splits at a hyphen, texts that
   need *fewer* lines, and codes that the Chromium reference itself shows reversed are listed as
   informational. Sheets and pairs are for looking at the result.

## Known limitations

- Fidelity is verified against **LibreOffice**; PowerPoint lays out text with its own engine, so line
  breaks and the vertical calibration can differ by a few pixels there (the width slack absorbs most of it).
  The fonts in `fonts/` must be installed where the PPTX is opened, otherwise PowerPoint substitutes them.
- Font weights: PowerPoint has only bold on/off. Weight ≥ 600 is bold (drawn with the Bold face, a bit
  heavier/wider than SemiBold 600); 500 is regular; Alexandria 800 is drawn as Bold (700).
  Alexandria is a variable font: LibreOffice embeds it as Type 3 in the PDF; older PowerPoint versions may
  show only its default instance.
- `box-shadow`, gradients, `transform`, filters and blend modes are not converted; borders other than
  solid/dashed/dotted are drawn solid; a single-side border on a rounded box is drawn as a straight rule.
- Images inside `overflow:hidden` boxes are not clipped (boxes are); rounded corners on `contain` images
  are only kept when the picture fills its box.
- Each paragraph is one PowerPoint paragraph (`<br>` → line break); lists (`ul/ol`) are kept as plain text.
- A table cell's own `padding`/`text-align` are used, but no colspan/rowspan (the deck subset has none).
- The QA check uses up to 127 QA colours per slide; more text boxes than that are not checked
  (a warning is printed).
- In the v39 source, codes after Arabic text carry no LRM, so the **Chromium reference** shows e.g.
  `2-9-1` as `1-9-2`; the PPTX shows them left-to-right (listed as info in the report). Newer sources
  carry LRMs, which are kept as they are.
