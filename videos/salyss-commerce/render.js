// usage: node render.js preview 1.5 4 7 ...   -> PNG stills in preview/
//        node render.js video out.mp4          -> silent H.264 video (30 fps)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

(async () => {
  const [mode, ...args] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await page.goto('file://' + path.join(__dirname, 'index.html'));
  await page.evaluate(async () => { await Promise.all([...document.fonts].map(f => f.load())); await document.fonts.ready; });
  await page.waitForTimeout(300);
  const cdp = await page.context().newCDPSession(page);
  const shot = async (fmt) => Buffer.from((await cdp.send('Page.captureScreenshot', { format: fmt, quality: fmt === 'jpeg' ? 93 : undefined })).data, 'base64');

  if (mode === 'preview') {
    fs.mkdirSync(path.join(__dirname, 'preview'), { recursive: true });
    for (const t of args.map(Number)) {
      await page.evaluate(t => window.render(t), t);
      fs.writeFileSync(path.join(__dirname, 'preview', `t${t.toFixed(2)}.png`), await shot('png'));
    }
  } else {
    const out = args[0] || 'silent.mp4';
    const fps = 30, dur = await page.evaluate(() => window.DURATION);
    const N = Math.round(fps * dur);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    const t0 = Date.now();
    for (let f = 0; f < N; f++) {
      await page.evaluate(t => window.render(t), f / fps);
      const buf = await shot('jpeg');
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (f % 150 === 0) console.log(`frame ${f}/${N}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
    console.log('done', out);
  }
  await browser.close();
})();
