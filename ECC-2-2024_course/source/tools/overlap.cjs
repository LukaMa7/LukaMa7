// Flags text elements that overlap each other or run past the slide edge in the Chromium render of reference.html
// usage: node overlap.cjs reference.html
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + require('path').resolve(process.argv[2])); await p.waitForTimeout(1500);
  const out = await p.evaluate(() => {
    const res = [];
    [...document.querySelectorAll('section')].forEach((s, si) => {
      const S = s.getBoundingClientRect();
      const els = [...s.querySelectorAll('p,h1,h2,h3,td,th,li')].filter(e => !e.closest('aside') && e.textContent.trim());
      const boxes = els.map(e => {
        const rg = document.createRange(); rg.selectNodeContents(e);
        const rs = [...rg.getClientRects()].filter(r => r.width > 1 && r.height > 1);
        return rs.map(r => ({ x0: r.left - S.left, y0: r.top - S.top, x1: r.right - S.left, y1: r.bottom - S.top }));
      });
      els.forEach((e, i) => boxes[i].forEach(r => { if (r.y1 > 1080 + 1 || r.x0 < -1 || r.x1 > 1921) res.push([si + 1, s.id, 'off-slide', e.textContent.trim().slice(0, 50)]); }));
      for (let i = 0; i < els.length; i++) for (let j = i + 1; j < els.length; j++) {
        if (els[i].contains(els[j]) || els[j].contains(els[i])) continue;
        pair: for (const a of boxes[i]) for (const c of boxes[j]) {
          const w = Math.min(a.x1, c.x1) - Math.max(a.x0, c.x0), h = Math.min(a.y1, c.y1) - Math.max(a.y0, c.y0);
          if (w > 4 && h > 4) { res.push([si + 1, s.id, 'overlap', els[i].textContent.trim().slice(0, 40) + ' <> ' + els[j].textContent.trim().slice(0, 40)]); break pair; }
        }
      }
    });
    return res;
  });
  console.log(JSON.stringify(out)); await b.close();
})();
