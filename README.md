# Claude Code kursi

Claude Code’ni professional darajada ishlatish bo‘yicha bepul o‘zbekcha kurs.
Sayt: https://dinmuhammad.uz/claude-code/

| # | Dars | Holat |
| --- | --- | --- |
| 1 | Claude Code qanday ishlaydi: agent sikli | tayyor |
| 2 | O‘rnatish, muhitlar va birinchi seans | tayyor |
| 3 | Ruxsatlar, rejimlar va sandbox | tayyor |
| 4 | Kontekst oynasi: compact, clear va rewind | rejada |
| 5 | CLAUDE.md va xotira | rejada |
| 6 | Vazifani qo‘yish: o‘rganish → reja → kod | rejada |
| 7 | Tekshirish: test, review va “ishonch, lekin tekshir” | rejada |
| 8 | Git, worktree va parallel sessiyalar | rejada |
| 9 | Katta va eski kod bazasi bilan ishlash | rejada |
| 10 | Slash buyruqlar va Skills | rejada |
| 11 | Subagentlar va parallel ish | rejada |
| 12 | Hooks va settings.json | rejada |
| 13 | MCP: tashqi tizimlarni ulash | rejada |
| 14 | Plaginlar va marketplace’lar | rejada |
| 15 | Headless rejim, CI va GitHub | rejada |
| 16 | Xavfsizlik, model tanlash va narx | rejada |

## Tuzilma

- `app/darslar/<slug>/page.mdx` — dars matni; `layout.tsx` — umumiy `CourseShell`.
- `components/lesson/` — darslardagi bloklar (`Session`, `Calc`, `Check`, `Download`…).
- `amaliyot/<slug>/<loyiha>/` — amaliyot fayllari; build vaqtida `out/amaliyot/<loyiha>.zip` bo‘ladi.
- `docs/manba/` — rasmiy hujjatlardan tekshirilgan faktlar (darslar shularga tayanadi).

## Ishga tushirish

```bash
npm ci
npm run dev
NEXT_PUBLIC_BASE_PATH=/claude-code npm run build   # out/ — statik sayt
```

Mustaqil o‘quv loyihasi: Anthropic bilan bog‘liq emas. “Claude” va “Claude Code” —
Anthropic’ning tovar belgilari.

Litsenziya: kod — MIT, dars matnlari — CC BY-NC 4.0.
