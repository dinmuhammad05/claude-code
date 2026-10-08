export type LessonStatus = "tayyor" | "yozilmoqda" | "rejada";

export type Lesson = {
  /** Tartib raqami — sayt bo'ylab bir xil ketma-ketlik */
  order: number;
  slug: string;
  /** Dars sarlavhasi */
  title: string;
  /** Bir gapda: darsda nima o'rganiladi */
  summary: string;
  /** Kartochka va skin uchun asosiy rang */
  accent: string;
  status: LessonStatus;
  level: "boshlang'ich" | "o'rta" | "murakkab";
  /** Taxminiy o'qish vaqti, daqiqa */
  minutes: number;
  /** Darsning kalit tushunchalari */
  topics: string[];
  /** Nashr va oxirgi tahrir sanasi (YYYY-MM-DD) — qidiruv tizimlari uchun */
  published?: string;
  updated?: string;
};

/**
 * Ketma-ketlik: asosdan professional ish usuliga, keyin kengaytirish va avtomatlashtirishga.
 */
export const lessons: Lesson[] = [
  {
    order: 1,
    slug: "agent",
    title: "Claude Code qanday ishlaydi: agent sikli",
    summary:
      "Chat va agent farqi: model o‘ylaydi, asbob chaqiradi, natijani ko‘radi va yana o‘ylaydi. Kursning qolgan hamma darslari tayanadigan aqliy model — raqamlar va real sessiya misoli bilan.",
    accent: "#d97757",
    status: "tayyor",
    level: "boshlang'ich",
    minutes: 60,
    topics: ["Agent sikli", "Asboblar (tools)", "Token", "Kontekst oynasi", "Tekshiriladigan maqsad"],
    published: "2026-10-08",
    updated: "2026-10-08",
  },
  {
    order: 2,
    slug: "ornatish",
    title: "O‘rnatish, muhitlar va birinchi seans",
    summary:
      "Terminal, VS Code, JetBrains, desktop, web va mobil: qaysi biri qachon kerak. O‘rnatish, kirish, yangilanish va birinchi haqiqiy vazifa.",
    accent: "#e0a458",
    status: "tayyor",
    level: "boshlang'ich",
    minutes: 50,
    topics: ["O‘rnatish", "Autentifikatsiya", "IDE", "Cloud sessiyalar", "claude doctor"],
    published: "2026-10-08",
    updated: "2026-10-08",
  },
  {
    order: 3,
    slug: "ruxsatlar",
    title: "Ruxsatlar, rejimlar va sandbox",
    summary:
      "Nimaga ruxsat berish kerak va nimaga yo‘q: permission rejimlari, allow/ask/deny qoidalari, plan mode, sandbox — va nega CLAUDE.md xavfsizlik chegarasi emas.",
    accent: "#c96442",
    status: "tayyor",
    level: "o'rta",
    minutes: 60,
    topics: ["Permission modes", "Allow/deny qoidalari", "Plan mode", "Sandbox", "Himoyalangan yo‘llar"],
    published: "2026-10-08",
    updated: "2026-10-08",
  },
  {
    order: 4,
    slug: "kontekst",
    title: "Kontekst oynasi: compact, clear va rewind",
    summary:
      "Nega uzun sessiya “aqlsizlanadi”: kontekst qanday to‘ladi, /context, /compact, /clear, /rewind va checkpointlar, sessiyani davom ettirish.",
    accent: "#b8860b",
    status: "rejada",
    level: "o'rta",
    minutes: 60,
    topics: ["Kontekst oynasi", "/compact", "/clear", "Checkpoint", "Sessiyani davom ettirish"],
  },
  {
    order: 5,
    slug: "claude-md",
    title: "CLAUDE.md va xotira",
    summary:
      "Loyiha qoidalarini Claude’ga bir marta o‘rgatish: CLAUDE.md ierarxiyasi, importlar, rules, avtomatik xotira — nimani yozish va nimani yozmaslik.",
    accent: "#cc785c",
    status: "rejada",
    level: "o'rta",
    minutes: 55,
    topics: ["CLAUDE.md", "Importlar", "Rules", "Auto memory", "/init"],
  },
  {
    order: 6,
    slug: "vazifa",
    title: "Vazifani qo‘yish: o‘rganish → reja → kod",
    summary:
      "Professional ish usuli: aniq vazifa, misollar va cheklovlar, plan mode, intervyu orqali spetsifikatsiya, kontekstni toza tutish.",
    accent: "#d4a27f",
    status: "rejada",
    level: "o'rta",
    minutes: 60,
    topics: ["Spetsifikatsiya", "Plan mode", "@-havolalar", "Intervyu", "Kursni tuzatish"],
  },
  {
    order: 7,
    slug: "tekshirish",
    title: "Tekshirish: test, review va “ishonch, lekin tekshir”",
    summary:
      "Kursning yuragi: Claude’ga tekshiriladigan maqsad berish, test birinchi, mustaqil review, Stop hook va /goal bilan “tugadi”ni isbotlash.",
    accent: "#e07a5f",
    status: "rejada",
    level: "o'rta",
    minutes: 70,
    topics: ["Test birinchi", "Code review", "Stop hook", "Yozuvchi va tekshiruvchi", "Mutatsiya"],
  },
  {
    order: 8,
    slug: "git",
    title: "Git, worktree va parallel sessiyalar",
    summary:
      "Commit, branch va PR’ni Claude bilan; worktree’lar va parallel sessiyalar; xatodan qaytish — rewind va git qachon kerak.",
    accent: "#bf8b5e",
    status: "rejada",
    level: "o'rta",
    minutes: 55,
    topics: ["Commit va PR", "Worktree", "Parallel sessiyalar", "/batch", "Attribution"],
  },
  {
    order: 9,
    slug: "katta-loyiha",
    title: "Katta va eski kod bazasi bilan ishlash",
    summary:
      "Notanish loyihaga kirish, arxitekturani o‘rganish, katta refaktor va migratsiyani bo‘laklarga bo‘lish, xavfni nazorat qilish.",
    accent: "#a3684a",
    status: "rejada",
    level: "murakkab",
    minutes: 65,
    topics: ["Kod bazasini o‘rganish", "Refaktor", "Migratsiya", "Explore subagent", "Bosqichma-bosqich"],
  },
  {
    order: 10,
    slug: "skills",
    title: "Slash buyruqlar va Skills",
    summary:
      "Takrorlanadigan ishni bitta buyruqqa aylantirish: SKILL.md tuzilishi, frontmatter, argumentlar, dinamik kontekst va qachon skill kerak emas.",
    accent: "#d98e5f",
    status: "rejada",
    level: "o'rta",
    minutes: 55,
    topics: ["Skills", "SKILL.md", "Slash buyruqlar", "Argumentlar", "Plaginlar"],
  },
  {
    order: 11,
    slug: "subagentlar",
    title: "Subagentlar va parallel ish",
    summary:
      "Kontekstni tejash va ishni bo‘lish: o‘rnatilgan Explore va Plan, o‘z agentingiz, model va asboblarni cheklash, izolyatsiya.",
    accent: "#c2703d",
    status: "rejada",
    level: "murakkab",
    minutes: 60,
    topics: ["Subagentlar", "Explore", "Agent ta’rifi", "Parallelizm", "Worktree izolyatsiyasi"],
  },
  {
    order: 12,
    slug: "hooks",
    title: "Hooks va settings.json",
    summary:
      "“Har safar, istisnosiz” bo‘lishi kerak bo‘lgan narsalar: hook hodisalari, matcherlar, exit 2, JSON javob va sozlamalar ierarxiyasi.",
    accent: "#b5651d",
    status: "rejada",
    level: "murakkab",
    minutes: 65,
    topics: ["Hooks", "PreToolUse", "Stop hook", "settings.json", "Ierarxiya"],
  },
  {
    order: 13,
    slug: "mcp",
    title: "MCP: tashqi tizimlarni ulash",
    summary:
      "GitHub, ma’lumotlar bazasi, brauzer va boshqa xizmatlarni ulash: transportlar, scope’lar, .mcp.json, ruxsatlar va prompt injection xavfi.",
    accent: "#d9a066",
    status: "rejada",
    level: "murakkab",
    minutes: 55,
    topics: ["MCP", "Transport", "Scope", "Tool search", "Prompt injection"],
  },
  {
    order: 14,
    slug: "plaginlar",
    title: "Plaginlar va marketplace’lar",
    summary:
      "Skills, subagentlar, hooks va MCP’ni bitta paketga yig‘ish: plagin tuzilishi, o‘rnatish va scope’lar, o‘z marketplace’ingiz, jamoaga tarqatish, plugin eval va xavfsizlik.",
    accent: "#cf7a52",
    status: "rejada",
    level: "murakkab",
    minutes: 60,
    topics: ["Plugin", "plugin.json", "Marketplace", "--plugin-dir", "Plugin eval"],
  },
  {
    order: 15,
    slug: "headless",
    title: "Headless rejim, CI va GitHub",
    summary:
      "claude -p bilan avtomatlashtirish, JSON chiqish, GitHub Actions va avtomatik code review — kuzatuvsiz ishlashning xavfsiz usullari.",
    accent: "#c27c4e",
    status: "rejada",
    level: "murakkab",
    minutes: 60,
    topics: ["claude -p", "GitHub Actions", "Code review", "--bare", "Budjet chegarasi"],
  },
  {
    order: 16,
    slug: "xavfsizlik-narx",
    title: "Xavfsizlik, model tanlash va narx",
    summary:
      "Sirlar, ishonchsiz repolar, prompt injection; model va effort tanlash, fast mode, /usage — va yakuniy loyiha.",
    accent: "#e08e45",
    status: "rejada",
    level: "murakkab",
    minutes: 70,
    topics: ["Xavfsizlik", "Model tanlash", "Effort", "Narx", "Yakuniy loyiha"],
  },
];

export const lessonBySlug = (slug: string) => lessons.find((l) => l.slug === slug);

export const readyLessons = () => lessons.filter((l) => l.status === "tayyor");

export function neighbours(slug: string) {
  const i = lessons.findIndex((l) => l.slug === slug);
  return {
    prev: i > 0 ? lessons[i - 1] : undefined,
    next: i >= 0 && i < lessons.length - 1 ? lessons[i + 1] : undefined,
  };
}

/**
 * Qorong"i brend ranglari (Uber qora, Slack to"q siyohrang) qora fonda o'qilmaydi.
 * Shu sabab yorug'ligi past ranglar oq tomonga aralashtiriladi.
 */
export function readableAccent(hex: string): string {
  const m = /^#([0-9a-f]{6})$/i.exec(hex);
  if (!m) return hex;
  const n = parseInt(m[1], 16);
  const [r, g, b] = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => {
    const c = v / 255;
    return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  const luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b;
  return luminance < 0.18 ? `color-mix(in oklab, ${hex} 55%, white)` : hex;
}
