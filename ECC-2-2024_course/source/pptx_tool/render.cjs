// Chromium side of build_pptx.py (run by it; not meant to be called by hand).
//
// For every slide: build a 1920x1080 wrapper page around the <section>, inject
// the icon SVGs, screenshot it (reference PNG), walk the rendered DOM
// (getBoundingClientRect + getComputedStyle) into a JSON list of paint items,
// then repaint every text element in a unique "QA colour" on white and
// screenshot again (used by the overflow check). Afterwards: rasterize the
// icons at 4x with a transparent background and print the reference PDF.
//
// usage: node render.cjs job.json      (job.json is written by build_pptx.py)
'use strict';
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const W = 1920, H = 1080;

// ---------------------------------------------------------------- page CSS
// Emulates the slide host: fixed 1920x1080 section, inline-style subset where
// a div/section without `display` is a flex column, tag defaults for h1-h3,
// ruled tables with 0.35em 0.6em cell padding, <aside> = notes (hidden).
const BASE_CSS = `
${job.fontCss}
html, body { margin: 0; padding: 0; background: #ffffff; }
section { position: relative; width: ${W}px; height: ${H}px; box-sizing: border-box; overflow: hidden; }
section:not([style*="display"]) { display: flex; flex-direction: column; }
section * { box-sizing: border-box; margin: 0; }
section div:not([style*="display"]) { display: flex; flex-direction: column; }
h1 { font-size: 96px; font-weight: 600; line-height: 1.1; }
h2 { font-size: 64px; font-weight: 600; line-height: 1.15; }
h3 { font-size: 44px; font-weight: 600; line-height: 1.2; }
table { border-collapse: collapse; width: 100%; }
th, td { padding: 0.35em 0.6em; }
aside { display: none !important; }
x-icon, x-shape { display: block; }
x-icon > svg, x-shape > svg { display: block; width: 100%; height: 100%; overflow: visible; }
`;

const PRINT_CSS = `
@page { size: ${W}px ${H}px; margin: 0; }
section { break-after: page; page-break-after: always; }
section:last-of-type { break-after: auto; page-break-after: auto; }
`;

function iconSvg(name) {
  const file = job.icons[name];
  if (!file) return null;
  let svg = fs.readFileSync(file, 'utf8');
  svg = svg.replace(/<\?xml[^>]*>/, '').trim();
  // size to the x-icon box, tint with currentColor
  svg = svg.replace(/<svg\b/, '<svg width="100%" height="100%" preserveAspectRatio="xMidYMid meet"');
  return svg;
}
const ICON_SVG = {};
for (const n of Object.keys(job.icons)) ICON_SVG[n] = iconSvg(n);

function slideMarkup(file) {
  let html = fs.readFileSync(file, 'utf8');
  html = html.replace(/src="\/_blob\/([0-9A-Za-z_-]+)"/g, (m, id) => {
    const p = job.blobs[id];
    if (!p) return `data-blob="${id}" data-missing="1" src=""`;
    return `data-blob="${id}" src="${pathToFileURL(p).href}"`;
  });
  return html;
}

function wrapper(sectionsHtml, extraCss) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>${BASE_CSS}${extraCss || ''}</style></head><body>${sectionsHtml}</body></html>`;
}

// ---------------------------------------------------------------- in-page code
// prepare(): icons -> inline SVG, x-shape -> SVG, table cell rules; wait fonts/images.
async function prepare(ICON_SVG) {
  // a hidden slide is still converted (and marked hidden in the PPTX)
  for (const sec of document.querySelectorAll('section[hidden]')) { sec.removeAttribute('hidden'); sec.dataset.wasHidden = '1'; }
  for (const el of document.querySelectorAll('x-icon')) {
    const svg = ICON_SVG[el.getAttribute('name')];
    if (svg) el.innerHTML = svg; else el.setAttribute('data-unknown', '1');
  }
  for (const el of document.querySelectorAll('x-shape')) {
    const cs = getComputedStyle(el);
    const fill = cs.backgroundColor;
    el.dataset.fill = fill;
    el.style.background = 'transparent';
    const r = el.getBoundingClientRect();
    const w = r.width, h = r.height, kind = el.getAttribute('kind') || 'rect';
    let shape = '';
    const hl = (L, S) => Math.min(0.4 * L, S * 1.0);   // head length
    if (kind === 'arrow-left' || kind === 'arrow-right') {
      const a = Math.min(0.4 * w, w), t0 = h * 0.25, t1 = h * 0.75;
      let pts = [[0, h / 2], [a, 0], [a, t0], [w, t0], [w, t1], [a, t1], [a, h]];
      if (kind === 'arrow-right') pts = pts.map(([x, y]) => [w - x, y]);
      shape = `<polygon points="${pts.map(p => p.join(',')).join(' ')}" fill="${fill}"/>`;
    } else if (kind === 'arrow-up' || kind === 'arrow-down') {
      const a = Math.min(0.4 * h, h), t0 = w * 0.25, t1 = w * 0.75;
      let pts = [[w / 2, 0], [w, a], [t1, a], [t1, h], [t0, h], [t0, a], [0, a]];
      if (kind === 'arrow-down') pts = pts.map(([x, y]) => [x, h - y]);
      shape = `<polygon points="${pts.map(p => p.join(',')).join(' ')}" fill="${fill}"/>`;
    } else if (kind === 'ellipse') {
      shape = `<ellipse cx="${w / 2}" cy="${h / 2}" rx="${w / 2}" ry="${h / 2}" fill="${fill}"/>`;
    } else if (kind === 'diamond') {
      shape = `<polygon points="${w / 2},0 ${w},${h / 2} ${w / 2},${h} 0,${h / 2}" fill="${fill}"/>`;
    } else {
      shape = `<rect x="0" y="0" width="${w}" height="${h}" fill="${fill}"/>`;
    }
    el.innerHTML = `<svg viewBox="0 0 ${w} ${h}" width="100%" height="100%">${shape}</svg>`;
  }
  // every cell is ruled on four sides in the table's border colour
  for (const t of document.querySelectorAll('table')) {
    const cs = getComputedStyle(t);
    const c = (cs.borderTopStyle !== 'none' && parseFloat(cs.borderTopWidth) > 0) ? cs.borderTopColor : 'rgba(0,0,0,0.15)';
    for (const cell of t.querySelectorAll('th, td')) {
      if (!cell.style.border) cell.style.border = `1px solid ${c}`;
    }
  }
  await Promise.all([...document.fonts].map(f => f.load().catch(() => null)));
  await document.fonts.ready;
  await Promise.all([...document.images].map(img => img.complete ? null : new Promise(r => { img.onload = img.onerror = r; })));
  await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
}

// walk(): DOM -> paint items (in DOM order), coordinates relative to the section.
function walk(QA) {
  const sec = document.querySelector('section');
  const S = sec.getBoundingClientRect();
  const TEXT = new Set(['P', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'LI']);
  const SKIP = new Set(['ASIDE', 'SCRIPT', 'STYLE', 'BR']);
  const out = { id: sec.id, bg: getComputedStyle(sec).backgroundColor, items: [], warnings: [],
    hidden: sec.dataset.wasHidden === '1', transition: sec.getAttribute('data-transition') || null };
  const aside = sec.querySelector(':scope > aside') || sec.querySelector('aside');
  out.notes = aside ? aside.textContent : '';
  let qaN = 0;
  const nextQa = () => (qaN < QA.length ? QA[qaN++] : null);

  const R = (el) => { const r = el.getBoundingClientRect(); return { x: r.left - S.left, y: r.top - S.top, w: r.width, h: r.height }; };
  const px = (v) => parseFloat(v) || 0;
  function opacity(el) {
    let o = 1;
    for (let e = el; e && e !== document.documentElement; e = e.parentElement) o *= parseFloat(getComputedStyle(e).opacity);
    return o;
  }
  function radius(cs, w, h) {
    const one = (v) => {
      const s = String(v).split(' ')[0];
      if (s.endsWith('%')) return { pct: parseFloat(s) };
      return { px: parseFloat(s) || 0 };
    };
    return [one(cs.borderTopLeftRadius), one(cs.borderTopRightRadius), one(cs.borderBottomRightRadius), one(cs.borderBottomLeftRadius)];
  }
  function borders(cs) {
    const b = {};
    for (const side of ['Top', 'Right', 'Bottom', 'Left']) {
      const w = px(cs[`border${side}Width`]), st = cs[`border${side}Style`], c = cs[`border${side}Color`];
      if (w > 0 && st !== 'none' && st !== 'hidden') b[side.toLowerCase()] = { w, style: st, color: c };
    }
    return b;
  }
  const visibleColor = (c) => c && c !== 'transparent' && !/rgba\([^)]*,\s*0\)$/.test(c);
  // clip rectangle from overflow:hidden ancestors (with their corner radii)
  function clipOf(el) {
    let clip = null;
    for (let e = el.parentElement; e && e !== sec; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.overflow === 'visible' && cs.overflowX === 'visible') continue;
      const r = R(e);
      const bl = px(cs.borderLeftWidth), bt = px(cs.borderTopWidth), br = px(cs.borderRightWidth), bb = px(cs.borderBottomWidth);
      const c = { x: r.x + bl, y: r.y + bt, w: r.w - bl - br, h: r.h - bt - bb, radius: radius(cs, r.w, r.h).map(q => q.px != null ? Math.max(0, q.px - Math.max(bl, bt)) : Math.min(r.w, r.h) * q.pct / 100) };
      if (!clip) clip = c;
      else {
        const x0 = Math.max(clip.x, c.x), y0 = Math.max(clip.y, c.y);
        const x1 = Math.min(clip.x + clip.w, c.x + c.w), y1 = Math.min(clip.y + clip.h, c.y + c.h);
        clip = { x: x0, y: y0, w: Math.max(0, x1 - x0), h: Math.max(0, y1 - y0), radius: clip.radius };
      }
    }
    return clip;
  }
  function runsOf(el) {
    const runs = [];
    (function rec(node) {
      for (const ch of node.childNodes) {
        if (ch.nodeType === 3) {
          if (!ch.data) continue;
          const cs = getComputedStyle(ch.parentElement);
          runs.push({
            t: ch.data, color: cs.color, size: px(cs.fontSize), weight: parseInt(cs.fontWeight, 10) || 400,
            italic: cs.fontStyle === 'italic', family: cs.fontFamily, ls: cs.letterSpacing,
            ul: (cs.textDecorationLine || '').includes('underline'), strike: (cs.textDecorationLine || '').includes('line-through'),
            tt: cs.textTransform, ws: cs.whiteSpace,
          });
        } else if (ch.nodeType === 1) {
          if (ch.tagName === 'BR') { runs.push({ br: true }); continue; }
          if (getComputedStyle(ch).display === 'none') continue;
          rec(ch);
        }
      }
    })(el);
    return runs;
  }
  function lines(el, lh) {
    const rg = document.createRange();
    rg.selectNodeContents(el);
    const rs = [...rg.getClientRects()].filter(r => r.width > 0.5 && r.height > 0.5);
    const mids = [];
    let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
    for (const r of rs) {
      const m = r.top + r.height / 2;
      if (!mids.some(t => Math.abs(t - m) < lh * 0.5)) mids.push(m);
      x0 = Math.min(x0, r.left); x1 = Math.max(x1, r.right); y0 = Math.min(y0, r.top); y1 = Math.max(y1, r.bottom);
    }
    return { n: mids.length, box: rs.length ? { x: x0 - S.left, y: y0 - S.top, w: x1 - x0, h: y1 - y0 } : null };
  }
  function lineHeight(cs) {
    const v = cs.lineHeight;
    if (v === 'normal') return px(cs.fontSize) * 1.3;
    return px(v);
  }
  function textInfo(el, cs) {
    const lh = lineHeight(cs);
    const ln = lines(el, lh);
    const qa = nextQa();
    if (qa) el.dataset.qa = qa;
    return {
      runs: runsOf(el), align: cs.textAlign, dir: cs.direction, lh, fs: px(cs.fontSize), nlines: ln.n, tbox: ln.box,
      pad: [px(cs.paddingTop), px(cs.paddingRight), px(cs.paddingBottom), px(cs.paddingLeft)],
      ws: cs.whiteSpace, valign: cs.verticalAlign, qa,
    };
  }
  function paint(el, cs, r) {
    const fill = visibleColor(cs.backgroundColor) ? cs.backgroundColor : null;
    const b = borders(cs);
    const shadow = cs.boxShadow && cs.boxShadow !== 'none' ? cs.boxShadow : null;
    return { fill, borders: b, radius: radius(cs, r.w, r.h), shadow, painted: !!(fill || Object.keys(b).length) };
  }

  // host = nearest painted ancestor box (a card, pill row...) or the slide: text may not grow beyond it
  function visit(el, host) {
    if (SKIP.has(el.tagName)) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const r = R(el);
    const tag = el.tagName;
    const base = { tag, ...r, opacity: opacity(el), clip: clipOf(el), host };
    if (tag === 'X-ICON') {
      out.items.push({ type: 'icon', ...base, name: el.getAttribute('name'), color: cs.color, svg: el.innerHTML, known: !el.dataset.unknown });
      return;
    }
    if (tag === 'X-SHAPE') {
      out.items.push({ type: 'shape', ...base, kind: el.getAttribute('kind') || 'rect', color: el.dataset.fill, borders: borders(cs) });
      return;
    }
    if (tag === 'svg' || tag === 'SVG') {
      out.items.push({ type: 'icon', ...base, name: 'svg', color: cs.color, svg: el.outerHTML, known: true });
      return;
    }
    if (tag === 'IMG') {
      out.items.push({ type: 'img', ...base, blob: el.dataset.blob || null, src: el.currentSrc || el.src, nw: el.naturalWidth, nh: el.naturalHeight,
        fit: cs.objectFit, pos: cs.objectPosition, radius: radius(cs, r.w, r.h), borders: borders(cs), missing: !!el.dataset.missing });
      return;
    }
    if (tag === 'TABLE') {
      const tb = borders(cs);
      const rows = [...el.rows].map(tr => {
        const tcs = getComputedStyle(tr);
        return {
          ...R(tr), bg: visibleColor(tcs.backgroundColor) ? tcs.backgroundColor : null,
          cells: [...tr.cells].map(td => {
            const ccs = getComputedStyle(td);
            return { tag: td.tagName, ...R(td), ...textInfo(td, ccs), fill: visibleColor(ccs.backgroundColor) ? ccs.backgroundColor : null, borders: borders(ccs) };
          }),
        };
      });
      out.items.push({ type: 'table', ...base, borders: tb, fill: visibleColor(cs.backgroundColor) ? cs.backgroundColor : null, rows, radius: radius(cs, r.w, r.h) });
      return;
    }
    if (TEXT.has(tag)) {
      if (r.w < 0.5 || r.h < 0.5) return;
      out.items.push({ type: 'text', ...base, ...paint(el, cs, r), ...textInfo(el, cs) });
      return;
    }
    if (el !== sec && r.w > 0.5 && r.h > 0.5) {
      const p = paint(el, cs, r);
      if (p.painted) { out.items.push({ type: 'box', ...base, ...p }); host = r; }
      // stray text directly inside a container (outside the subset) -> keep it as text
      const stray = [...el.childNodes].some(n => n.nodeType === 3 && n.data.trim());
      if (stray) out.warnings.push(`text directly inside <${tag.toLowerCase()}> (kept as one text box)`);
      if (stray) { out.items.push({ type: 'text', ...base, fill: null, borders: {}, radius: radius(cs, r.w, r.h), painted: false, ...textInfo(el, cs) }); return; }
    }
    for (const ch of el.children) visit(ch, host);
  }
  visit(sec, { x: 0, y: 0, w: S.width, h: S.height });
  if (qaN >= QA.length) out.warnings.push('more text boxes than QA colours: some are not checked');
  return out;
}

// diag(): paint every QA-tagged text in its colour, everything else invisible, on white.
function diag() {
  const st = document.createElement('style');
  st.textContent = `
    section, section * { background: transparent !important; border-color: transparent !important; box-shadow: none !important;
      text-shadow: none !important; opacity: 1 !important; color: transparent !important; -webkit-text-stroke: 0 !important; }
    section { background: #ffffff !important; }
    section img, section x-icon, section x-shape, section svg { visibility: hidden !important; }
    section [data-qa], section [data-qa] * { color: var(--qa) !important; }`;
  document.head.appendChild(st);
  for (const el of document.querySelectorAll('[data-qa]')) el.style.setProperty('--qa', el.dataset.qa);
}

(async () => {
  const browser = await chromium.launch({ args: ['--font-render-hinting=none', '--disable-lcd-text'] });
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  page.on('pageerror', e => console.error('pageerror', e.message));
  const tmp = path.join(job.workDir, 'page.html');
  const results = [];
  for (const s of job.slides) {
    fs.writeFileSync(tmp, wrapper(slideMarkup(s.file)));
    await page.goto(pathToFileURL(tmp).href, { waitUntil: 'load' });
    await page.evaluate(prepare, ICON_SVG);
    await page.screenshot({ path: s.refPng, clip: { x: 0, y: 0, width: W, height: H } });
    const data = await page.evaluate(walk, job.qaColors);
    data.index = s.index;
    if (s.diagPng) {
      await page.evaluate(diag);
      await page.screenshot({ path: s.diagPng, clip: { x: 0, y: 0, width: W, height: H } });
    }
    results.push(data);
    process.stdout.write(`\rrendered ${results.length}/${job.slides.length} ${s.id}            `);
  }
  process.stdout.write('\n');

  // icons -> PNG at 4x, transparent background
  const icons = {};
  const ictx = await browser.newContext({ viewport: { width: 1200, height: 1200 }, deviceScaleFactor: 4 });
  const ip = await ictx.newPage();
  await ip.setContent('<!doctype html><html><body style="margin:0;background:transparent"><div id="i"></div></body></html>');
  let k = 0;
  for (const d of results) {
    for (const it of d.items) {
      if (it.type !== 'icon' || !it.known) continue;
      const w = Math.max(1, Math.round(it.w * 100) / 100), h = Math.max(1, Math.round(it.h * 100) / 100);
      const key = `${it.svg}|${it.color}|${w}|${h}`;
      if (!icons[key]) {
        const file = path.join(job.iconDir, `icon${String(++k).padStart(3, '0')}.png`);
        await ip.evaluate(([svg, color, w, h]) => {
          const d = document.getElementById('i');
          d.style.cssText = `width:${w}px;height:${h}px;color:${color}`;
          d.innerHTML = svg;
          const s = d.querySelector('svg');
          if (s) { s.setAttribute('width', '100%'); s.setAttribute('height', '100%'); s.style.display = 'block'; }
        }, [it.svg, it.color, w, h]);
        await ip.locator('#i').screenshot({ path: file, omitBackground: true });
        icons[key] = file;
      }
      it.png = icons[key];
      delete it.svg;
    }
  }
  await ictx.close();

  // reference PDF straight from Chromium, one 1920x1080 page per slide
  if (job.refPdf) {
    const all = job.slides.map(s => slideMarkup(s.file)).join('\n');
    const pdfHtml = path.join(job.workDir, 'reference.html');
    fs.writeFileSync(pdfHtml, wrapper(all, PRINT_CSS));
    const pctx = await browser.newContext({ viewport: { width: W, height: H } });
    const pp = await pctx.newPage();
    await pp.goto(pathToFileURL(pdfHtml).href, { waitUntil: 'load' });
    await pp.evaluate(prepare, ICON_SVG);
    await pp.pdf({ path: job.refPdf, width: `${W}px`, height: `${H}px`, printBackground: true, preferCSSPageSize: true });
    await pctx.close();
  }
  await browser.close();
  fs.writeFileSync(job.outJson, JSON.stringify({ slides: results }, null, 0));
  console.log(`wrote ${job.outJson}`);
})().catch(e => { console.error(e); process.exit(1); });
