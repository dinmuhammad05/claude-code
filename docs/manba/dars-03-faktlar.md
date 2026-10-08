# 3-dars uchun tekshirilgan faktlar (2026-10-08)

Manba: code.claude.com/docs/en/ — permissions, permission-modes, sandboxing, settings,
settings-reference (qisman), security, auto-mode-config (xulosa orqali).

## Rejimlar
- `default` = Manual (alias `manual`): faqat o'qish so'rovsiz.
- `acceptEdits`: o'qish, fayl tahrirlari va ish papkasi ichida `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, `sed`.
- `plan`: o'qish (+ auto mavjud bo'lsa klassifikator tasdiqlagan buyruqlar); tahrir reja tasdiqlanguncha yo'q. Kirish: Shift+Tab, `/plan`, `--permission-mode plan`. Tasdiqlash: "Yes, and use auto mode" / "Yes, manually approve edits" / "No, keep planning". Ctrl+G — rejani muharrirda tahrirlash.
- `auto`: klassifikator (ikkinchi model) ko'rib chiqadi. v2.1.283+ da interaktiv terminal va VS Code uchun standart boshlang'ich rejim. "Auto mode reduces permission prompts but does not guarantee safety."
- `dontAsk`: so'rov chiqadigan hamma narsa rad etiladi; faqat `--permission-mode dontAsk`.
- `bypassPermissions`: so'rov va xavfsizlik tekshiruvlari o'chadi, himoyalangan yo'llarga yozish ham; deny qoidalari baribir ishlaydi. "Only use this mode in isolated environments like containers, VMs, or dev containers without internet access..." "offers no protection against prompt injection". root/sudo bilan ishlamaydi.
- Shift+Tab: auto → default → acceptEdits → plan → (bypass) → (auto). dontAsk aylanishda yo'q.
- `auto` va `bypassPermissions` ni `.claude/settings.json` / `settings.local.json` da defaultMode qilib bo'lmaydi.
- Auto: 3 ta ketma-ket yoki 20 ta jami bloklashdan keyin so'rovga qaytadi. Kirishda keng qoidalar (`Bash(*)`, `Bash(python*)` kabi interpretatorlar, paket menejer run) tashlab yuboriladi.
- Hech bir rejim avtomatik tasdiqlamaydi: ask qoidalari, AskUserQuestion, muhim yo'llarda rm/rmdir va boshqalar.
- Himoyalangan yo'llar: `.git`, `.vscode`, `.idea`, `.husky`, `.claude` (istisnolar bilan), `.bashrc`, `.zshrc`, `.profile`, `.npmrc`, `.mcp.json`, `.claude.json`, `.gitconfig` va boshqalar; `permissions.allow` ularni oldindan tasdiqlamaydi.

## Qoidalar
- "Rules are evaluated in order: deny, then ask, then allow. The first match in that order determines the outcome, and rule specificity doesn't change the order." "An allow rule can't carve an exception out of a deny rule."
- Deny'da yalang'och asbob nomi (`"Bash"`) asbobni kontekstdan olib tashlaydi.
- Bash `*` istalgan joyda, bo'sh joylar bilan ham. `Bash(ls *)` — `ls` va `ls -la`, `lsof` emas; `Bash(ls*)` — `lsof` ham. Oxirgi ` *` yagona yulduzcha bo'lsa yalang'och buyruqni ham qamraydi. `Bash(ls:*)` = `Bash(ls *)`.
- Murakkab buyruq ajratgichlari: `&&`, `||`, `;`, `|`, `|&`, `&`, yangi qator. Deny/ask istalgan qism buyruqqa (`$(...)` ichida ham). "A rule must match each subcommand independently."
- Olib tashlanadigan o'ramlar: `timeout`, `time`, `nice`, `nohup`, `stdbuf`, `command`, `builtin`, `noglob`, yalang'och `xargs`. `npx`, `docker exec`, `direnv exec` va boshqalar olib tashlanmaydi.
- Muhit o'zgaruvchisi prefiksi: deny/ask har qanday prefiksdan o'tib moslashadi; allow faqat ma'lum xavfsiz o'zgaruvchilardan (masalan `NODE_ENV`).
- "a deny or ask rule covers the invocation Claude usually produces and isn't a security boundary around the program." `Bash(curl *)` `/usr/bin/curl` yoki `sh -c 'curl ...'` ni to'xtatmaydi.
- O'qish uchun buyruqlar (`ls`, `cat`, `echo`, `pwd`, `head`, `tail`, `grep`, `find`, `wc`, `which`, `diff`, `stat`, `du`, `cd`, faqat o'qiydigan `git`) so'rovsiz; ask/deny bilan o'zgartirish mumkin.
- Read/Edit: gitignore sintaksisi; `//` mutlaq, `~/` uy, `/` sozlama manbasiga nisbatan, `./` yoki yalang'och — joriy papkaga nisbatan. `*` bitta segment, `**` chuqur. `.env` = `**/.env`.
- "`Edit` rules apply to all built-in tools that edit files." Read deny Edit/Write ni ham bloklaydi.
- Read/Edit deny Bash'dagi `cat`, `head`, `tail`, `sed`, `tee` va yo'naltirish nishonlariga ham amal qiladi; lekin `grep -r pattern .` yoki fayl ochadigan Python/Node skriptiga amal qilmaydi. `.claudeignore` ta'sirsiz.
- `WebFetch(domain:example.com)`; `*.example.com` — subdomenlar (apex emas). "using WebFetch alone doesn't prevent network access" — Bash ruxsat bo'lsa curl bor.
- "Yes, and don't ask again" — `.claude/settings.local.json` (git repo ildizida). Tahrir ruxsatlari saqlanmaydi.
- Ustuvorlik: managed > `--settings` > local > project > user. Ro'yxatlar birlashadi; istalgan darajadagi deny ustun.
- Loyiha `permissions.allow` workspace trust'dan keyin ishlaydi; deny va ask darhol.

## Sandbox
- Bash, PowerShell, Monitor buyruqlari va ularning bolalari; Read/Edit/WebFetch/MCP/hooks — sandbox'dan tashqarida.
- macOS (Seatbelt), Linux va WSL2 (bubblewrap + socat). Native Windows — yo'q.
- `/sandbox` yoki `sandbox.enabled: true`; standart o'chiq. Ish papkasi va vaqtinchalik papkaga yozish; tarmoq — proksi orqali, ruxsat etilgan domenlar boshida bo'sh.
- Sandbox ishga tushmasa, standart holatda buyruqlar sandboxsiz ishlaydi; `failIfUnavailable: true` — chiqib ketadi.
- Kalitlar: `enabled`, `failIfUnavailable`, `autoAllowBashIfSandboxed` (true), `excludedCommands`, `allowUnsandboxedCommands` (true), `filesystem.allowWrite/denyWrite/denyRead/allowRead`, `network.allowedDomains/deniedDomains`.
- `dangerouslyDisableSandbox` qayta urinishi; `allowUnsandboxedCommands: false` uni o'chiradi.
- "Sandboxing reduces risk but is not a complete isolation boundary." "Effective sandboxing requires both filesystem and network isolation."
