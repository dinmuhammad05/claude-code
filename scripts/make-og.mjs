#!/usr/bin/env node
/**
 * Ijtimoiy tarmoqlarda ulashish uchun preview rasmlar (1200x630) yasaydi:
 *   public/og.png            — bosh sahifa uchun
 *   public/og-<slug>.png     — har bir tayyor dars uchun
 *
 * Rasmlar repozitoriyga commit qilinadi, shuning uchun bu skript faqat
 * dizayn yoki darslar ro'yxati o'zgarganda kerak. Playwright talab qiladi:
 *   npx --yes playwright@latest install chromium && node scripts/make-og.mjs
 */
import { chromium } from "playwright";
import { writeFile, readFile } from "node:fs/promises";

const lessonsSrc = await readFile("lib/lessons.ts", "utf8");
const ready = [...lessonsSrc.matchAll(/order:\s*(\d+),\s*\n\s*slug:\s*"([^"]+)",\s*\n\s*title:\s*"([^"]+)",[\s\S]*?accent:\s*"([^"]+)",\s*\n\s*status:\s*"([^"]+)"/g)]
  .map((m) => ({ order: +m[1], slug: m[2], title: m[3], accent: m[4], status: m[5] }))
  .filter((l) => l.status === "tayyor");

const MARK = `<svg viewBox="0 0 512 512" width="96" height="96">
  <rect x="56" y="96" width="400" height="320" rx="48" fill="none" stroke="ACCENT" stroke-width="28"/>
  <path d="M150 210 L222 262 L150 314" fill="none" stroke="ACCENT" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M262 318 H360" fill="none" stroke="#f0eee6" stroke-width="32" stroke-linecap="round"/>
</svg>`;

const template = ({ accent, eyebrow, title, subtitle, footer }) => `
<body style="margin:0;width:1200px;height:630px;background:#141413;color:#f0eee6;
  font-family:ui-sans-serif,system-ui,'Segoe UI',Roboto,sans-serif;position:relative;overflow:hidden">
  <div style="position:absolute;inset:0;background:
    radial-gradient(900px 420px at 88% -10%, ${accent}26, transparent 60%),
    radial-gradient(700px 380px at -10% 110%, ${accent}1a, transparent 60%)"></div>
  <div style="position:absolute;left:0;top:0;width:100%;height:8px;background:${accent}"></div>
  <div style="position:relative;padding:70px 76px;height:100%;box-sizing:border-box;
    display:flex;flex-direction:column;justify-content:space-between">
    <div style="display:flex;align-items:center;gap:22px">
      ${MARK.replace(/ACCENT/g, accent)}
      <div style="font-size:26px;color:#a8a49a;font-weight:500">${eyebrow}</div>
    </div>
    <div>
      <div style="font-size:${title.length > 34 ? 62 : 76}px;font-weight:800;line-height:1.08;
        letter-spacing:-0.03em;max-width:1000px">${title}</div>
      <div style="margin-top:22px;font-size:29px;color:#a8a49a;max-width:900px;line-height:1.4">${subtitle}</div>
    </div>
    <div style="display:flex;align-items:center;gap:14px;font-size:23px;color:#8b949e;
      font-family:ui-monospace,Menlo,monospace">
      <span style="color:${accent}">${footer.left}</span>
      <span style="opacity:.4">·</span>
      <span>${footer.right}</span>
    </div>
  </div>
</body>`;

const browser = await chromium.launch({
  executablePath: process.env.PW_CHROMIUM ?? "/opt/pw-browsers/chromium",
});

async function shot(name, html) {
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  await page.setContent(html);
  await writeFile(`public/${name}`, await page.screenshot());
  await page.close();
  console.log(`public/${name}`);
}

await shot(
  "og.png",
  template({
    accent: "#d97757",
    eyebrow: "Claude Code kursi",
    title: "Claude Code’ni<br/>professional darajada",
    subtitle:
      "Agent sikli, kontekst, CLAUDE.md, tekshirish, subagentlar, hooks, MCP, plaginlar va CI — rasmiy hujjatlarga tayangan 16 dars",
    footer: { left: "bepul · o‘zbek tilida", right: "dinmuhammad.uz" },
  }),
);

for (const l of ready) {
  await shot(
    `og-${l.slug}.png`,
    template({
      accent: l.accent === "#000000" ? "#e8ecf1" : l.accent,
      eyebrow: `Claude Code kursi · dars ${String(l.order).padStart(2, "0")}`,
      title: l.title,
      subtitle: "Rasmiy hujjatlarga tayangan tushuntirish, real sessiya misollari va tekshiriladigan amaliyot",
      footer: { left: "bepul · o‘zbek tilida", right: "dinmuhammad.uz" },
    }),
  );
}

await browser.close();
