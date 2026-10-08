# Amaliyot: do‘kon — ruxsat qoidalarini yozish

Claude Code kursi, 3-dars. Faqat Python 3.9+ standart kutubxonasi kerak.

Siz kichik “do‘kon” loyihasi uchun **`.claude/settings.json`** ni yozasiz:
nimaga so‘rovsiz ruxsat, nimaga har doim so‘rash, nima umuman taqiqlangan.

| Fayl | Nima |
| --- | --- |
| `.claude/settings.json` | **Siz to‘ldirasiz** — hozir bo‘sh qoidalar |
| `ruxsat.py` | Ruxsat qoidalari simulyatori (Manual rejim). O‘zgartirmang |
| `tekshir.py` | Qabul tekshiruvi (9 ta). O‘zgartirmang |
| `src/`, `tests/` | Kod va testlar |
| `migrations/` | Bazaga ta’sir qiladigan migratsiyalar |
| `.env`, `secrets/` | **Soxta** sirlar — amaliyot uchun |
| `deploy.sh` | Soxta deploy skripti |

## Talablar

1. **Testlar** — `python -m unittest` (istalgan argument bilan) so‘rovsiz.
2. **Lint** — `ruff check` (istalgan argument bilan) so‘rovsiz.
3. **Git** — o‘qish (`status`, `diff`, `log`) so‘rovsiz; `git commit` har
   doim so‘raladi; `git push` taqiqlangan (istalgan argument bilan).
4. **Sirlar** — `.env` (istalgan papkada) va `secrets/` ichidagi hamma
   narsa: o‘qish ham, tahrir ham taqiqlangan.
5. **Xavfli buyruqlar** — `rm -rf ...` va `./deploy.sh ...` taqiqlangan.
   Oddiy `rm fayl` — odatdagidek so‘raladi.
6. **Kod** — `src/` va `tests/` ichidagi fayllarni tahrirlash so‘rovsiz;
   `migrations/` ichidagisi har doim so‘raladi.
7. **Veb** — `docs.python.org` so‘rovsiz; `pastebin.com` taqiqlangan.
8. **Birlashish** — hamkasbingizning `~/.claude/settings.json` ida
   `Bash(git *)` va `Edit(./**)` ruxsati bo‘lsa ham, 3, 4 va 6-talablar
   buzilmasin.

Umumiy: `Bash`, `Bash(*)`, `Bash(python *)` kabi **keng** ruxsatlar va
loyiha faylida `defaultMode: "auto"` yoki `"bypassPermissions"` bo‘lmasin.

## Qanday ishlash

```bash
python ruxsat.py Bash "git push origin main"   # bitta harakatni sinash
python ruxsat.py Read .env
python tekshir.py                              # hammasini tekshirish
```

## Topshiriqlar

1. **Qoidalarni yozing.** `.claude/settings.json` ni to‘ldiring va
   `python tekshir.py` → `Jami: 9/9 OK` ga yeting.
2. **Cheklovni ko‘ring.** `tekshir.py` oxiridagi “ma’lumot uchun” qatorlarini
   o‘qing: nega `git -C . push` yoki `grep -r` qoidalarga tushmaydi?
3. **Haqiqiy sessiyada sinang.** `git init && git add . && git commit -m boshlang‘ich`,
   keyin `claude --permission-mode default`:
   - `/permissions` — qoidalaringiz manbasi bilan ko‘rinadimi?
   - “`.env` faylini o‘qib ber” — agent rad javobini oladimi?
   - “testlarni ishga tushir” — so‘rovsiz ishladimi?
   - `Shift+Tab` bilan plan rejimiga o‘ting va “deploy jarayonini
     tushuntir” deng — tahrir bo‘lmasligini kuzating.
4. **Sandbox** (macOS, Linux yoki WSL 2): `/sandbox` ni yoqing va
   `curl https://example.com` ni ishga tushirtiring — tarmoq so‘rovi
   qanday so‘raladi?

## Tekshiruv mezoni

`python tekshir.py` oxirida `Jami: 9/9 OK`.
