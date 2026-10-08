/**
 * Loyihaning markaziy sozlamalari.
 * Muallif, havolalar va litsenziyani o'zgartirish uchun faqat shu faylni tahrirlang.
 */
export const site = {
  name: "Claude Code kursi",
  shortName: "Claude Code",
  tagline: "Claude Code’ni professional darajada ishlatish — o‘zbek tilida",
  description:
    "Bepul o‘zbekcha Claude Code kursi: agent qanday ishlaydi, ruxsatlar, kontekst, CLAUDE.md, tekshirish, Git, Skills, subagentlar, hooks, MCP, CI va xavfsizlik. Har bir dars rasmiy hujjatlarga tayanadi va amaliy mashq bilan.",
  /** GitHub Pages manzili — OG rasm va sitemap uchun mutlaq havolalar shu yerdan olinadi */
  url: "https://dinmuhammad.uz/claude-code",
  author: {
    handle: "dinmuhammad05",
    name: "Dinmuhammad",
    portfolio: "https://dinmuhammad.uz/",
    github: "https://github.com/dinmuhammad05",
    telegram: "@dinMuhammad05",
    telegramUrl: "https://t.me/dinMuhammad05",
  },
  /**
   * Kontentni himoyalash sozlamalari.
   *
   * DIQQAT: bularning hech biri jiddiy nusxa ko'chirishni to'xtata olmaydi.
   * Ular faqat tasodifiy nusxalashni qiyinlashtiradi va tarqalgan nusxada
   * manbani ko'rsatadi. Haqiqiy himoya faqat server tomonda autentifikatsiya
   * bilan bo'ladi — docs/HIMOYA.md ga qarang.
   */
  protection: {
    /** Qidiruv tizimlariga indekslashni taqiqlash (kurs bepul — indekslanadi) */
    noindex: false,
    /** "Barcha darslarni yuklab olish" tugmasi (offline nusxa) */
    offlineDownload: false,
    /** Nusxa ko'chirish va o'ng tugmani cheklash (kursda o'chiq: buyruq va kodni nusxalash kerak) */
    copyGuard: false,
    /** Chop etishni (Ctrl+P, PDF ga saqlash) to'sish */
    blockPrint: true,
    /** Sahifa ustida ko'rinmas suv belgisi */
    watermark: true,
  },
  license: {
    code: "MIT",
    content: "CC BY-NC 4.0",
    contentUrl: "https://creativecommons.org/licenses/by-nc/4.0/deed.uz",
  },
} as const;
