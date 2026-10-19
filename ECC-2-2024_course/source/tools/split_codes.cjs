// Lists control codes / dates / LTR tokens that a line break splits in the Chromium render of reference.html
// usage: node split_codes.cjs reference.html
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + require('path').resolve(process.argv[2])); await p.waitForTimeout(1500);
  const out = await p.evaluate(() => {
    const res = []; const re = /[0-9A-Za-z][0-9A-Za-z.:/–-]*[-–:/][0-9A-Za-z.:/–-]*[0-9A-Za-z%]/g;
    const secs = [...document.querySelectorAll('section')];
    secs.forEach((s, si) => {
      const w = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
      let n;
      while ((n = w.nextNode())) {
        if (n.parentElement.closest('aside')) continue;
        let m; re.lastIndex = 0;
        while ((m = re.exec(n.data))) {
          const r = document.createRange(); r.setStart(n, m.index); r.setEnd(n, m.index + m[0].length);
          const tops = new Set([...r.getClientRects()].filter(x => x.width > 0.5).map(x => Math.round(x.top / 8)));
          if (tops.size > 1) res.push([si + 1, s.id || s.getAttribute('data-id') || '', m[0], n.data.slice(Math.max(0, m.index - 30), m.index + m[0].length + 10)]);
        }
      }
    });
    return res;
  });
  console.log(JSON.stringify(out, null, 0)); await b.close();
})();
