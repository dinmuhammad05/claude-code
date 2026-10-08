# 2-dars va 14-dars (plaginlar) uchun tekshirilgan faktlar (2026-10-08)

Manba: code.claude.com/docs/en/ — setup, quickstart, platforms, authentication, vs-code,
jetbrains, claude-code-on-the-web, troubleshoot-install, terminal-config, commands, memory,
settings-reference, plugins/overview, plugins/create, plugins/install, plugins/manifest-reference,
plugins/create-marketplace, plugins/org, plugins/security, plugin-evals.
Iqtiboslar WebFetch matnidan; nashrdan oldin jonli sahifa bilan solishtiring.

## O'rnatish
- Talablar: macOS 13.0+; Windows 10 1809+ / Server 2019+; Ubuntu 20.04+; Debian 10+; Alpine 3.19+; 4 GB+ RAM; internet.
- Native (tavsiya): `curl -fsSL https://claude.ai/install.sh | bash`; PowerShell `irm https://claude.ai/install.ps1 | iex`; CMD `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`.
- Muqobil: `brew install --cask claude-code` (stable) / `claude-code@latest`; `winget install Anthropic.ClaudeCode`; `npm install -g @anthropic-ai/claude-code` (Node.js 22+), "Do NOT use `sudo npm install -g`".
- Kanallar: `latest` (standart), `stable` (~bir hafta eski). `/config` yoki `"autoUpdatesChannel": "stable"`.
- Native — fonda avto-yangilanish; Homebrew, WinGet, apt/dnf/apk — standart holatda yo'q.
- `claude --version`, `claude doctor` (sessiya ochmasdan diagnostika), `claude update`.
- O'chirish: `rm -f ~/.local/bin/claude`, `rm -rf ~/.local/share/claude`; `~/.claude` va `~/.claude.json` o'chirilsa sozlamalar, ruxsatlar, MCP va tarix ketadi.

## Kirish
- Pro, Max, Team, Enterprise yoki Console. Bepul claude.ai rejasida Claude Code yo'q. Bedrock/Vertex/Foundry ham.
- `claude` → brauzer; `c` URL ni nusxalaydi; `/login`, `/logout`, `/status`.
- Tuzoq: obuna bor va `ANTHROPIC_API_KEY` o'rnatilgan bo'lsa, tasdiqlangach API kalit ishlatiladi; yechim `unset ANTHROPIC_API_KEY` va `/status`.
- Bulut sessiyalari har doim obuna hisob ma'lumotlaridan foydalanadi.

## Muhitlar
- CLI: to'liq imkoniyat; skript va Agent SDK faqat CLI'da.
- Desktop: vizual review, parallel sessiyalar; Linux — beta.
- VS Code: 1.94.0+; kengaytma `claude` ni PATH ga qo'shmaydi.
- JetBrains: plagin IDE terminalida `claude` ni ishga tushiradi, CLI ni o'zi olib kelmaydi — ikkalasini o'rnatish kerak.
- Web: bulut VM, uzilgandan keyin ham ishlaydi; GitHub kerak; `/clear`, `/plugin`, `/resume` yo'q; lokal plaginlar yuklanmaydi.
- Mobil: bulut sessiyalari va Remote Control.

## Birinchi sessiya (quickstart)
- `cd loyiha && claude`; savollar: "what does this project do?", "where is the main entry point?", "explain the folder structure".
- `claude "vazifa"`, `claude -p`, `claude -c`, `claude -r`, `/clear`, `/help`, `/exit`.

## /init
- Kod bazasini tahlil qilib CLAUDE.md yozadi (build, test, konventsiyalar). Mavjud bo'lsa — ustidan yozmaydi, yaxshilash taklif qiladi.
- `CLAUDE_CODE_NEW_INIT=1` — interaktiv: CLAUDE.md, skills, hooks taklifi, yozishdan oldin ko'rib chiqish.

## Windows
- Native: Git for Windows ixtiyoriy, lekin Bash va Monitor uchun kerak; bo'lmasa PowerShell asbobi. Sandbox — native'da yo'q.
- WSL 2 — sandbox bor; WSL 1 — yo'q. `CLAUDE_CODE_GIT_BASH_PATH`.

## Terminal
- Yangi qator: Ctrl+J yoki `\` + Enter hamma joyda. Shift+Enter — Ghostty, Kitty, iTerm2, WezTerm, Warp, Apple Terminal, Windows Terminal.
- `/terminal-setup` — VS Code, Cursor, Alacritty (0.16 dan oldin), Zed uchun.
- `/theme`; vim: `/config` → Editor mode (`/vim` olib tashlangan).

## Sozlama fayllari
- `.claude/settings.local.json` — Claude Code yaratganda git'dan chetda qoldiradi; qo'lda yaratsangiz `.gitignore` ga o'zingiz qo'shing.
- `CLAUDE.local.md` ni `.gitignore` ga qo'shing.
- `~/.claude/settings.json` — foydalanuvchi; `~/.claude.json` — kirish, MCP, loyiha holati (qo'lda tahrirlash shart emas).
- Ustuvorlik: managed > CLI > local > project > user.

## Muammolar
- `command not found: claude` — PATH; `which -a claude` (bir nechta o'rnatish).
- `syntax error near unexpected token '<'` / 403 — skript o'rniga HTML.
- `EACCES`, TLS xatolari, `Killed` (xotira), `Raw mode is not supported`.
- `/doctor` — sozlash tekshiruvi (tuzatishlarni taklif qiladi); `/status` — versiya, model, akkaunt.

## Plaginlar
- Plagin — skills, agents, hooks, MCP va boshqa komponentlar bitta birlik sifatida o'rnatiladigan papka.
- Manifest: `.claude-plugin/plugin.json`, faqat `name` majburiy (kebab-case). Komponentlar ildizda: `skills/<nom>/SKILL.md`, `commands/` (eski), `agents/`, `hooks/hooks.json`, `.mcp.json`, `.lsp.json`, `output-styles/`, `bin/`, `settings.json`. `.claude-plugin/` ichiga faqat plugin.json.
- Qachon: bitta loyiha yoki faqat siz — standalone `.claude/`; jamoa, bir nechta loyiha, versiyalangan reliz — plagin.
- O'rnatish: `/plugin` (Discover), `/plugin install nom@marketplace`, `claude plugin install nom@marketplace --scope user|project|local` (standart user).
- Marketplace qo'shish: `/plugin marketplace add owner/repo` (#ref, lokal yo'l, git URL, marketplace.json URL).
- Rasmiy marketplace: `claude-plugins-official` (birinchi interaktiv ishga tushishda avtomatik). Community: `claude-community`. `anthropics/claude-code` — demo marketplace.
- Scope fayllari: user `~/.claude/settings.json`, project `.claude/settings.json`, local `.claude/settings.local.json`; local > project > user.
- Nom maydoni: `/<plagin>:<skill>`.
- Sinash: `claude plugin validate ./p`, `claude --plugin-dir ./p`, `/reload-plugins`, `claude plugin list`.
- Marketplace: `.claude-plugin/marketplace.json` — `name`, `owner.name`, `plugins[]` (`name`, `source`); manbalar: `./yo'l`, github, git-subdir, url, npm, archive.
- Jamoa: `.claude/settings.json` da `extraKnownMarketplaces` va `enabledPlugins`; managed: `strictKnownMarketplaces`, `blockedMarketplaces`.
- Xavfsizlik: "A Claude Code plugin you install can execute arbitrary code on your machine with your user privileges." Command hook va monitorlar ruxsat qoidalari va sandbox'dan tashqarida.
- Yoqilgan plagin skill va agent tavsiflarini har aylanishda kontekstga qo'shadi.
- Plugin eval: `claude plugin eval init`, `claude plugin eval .`; graderlar regex, tool_used, tool_order, file_exists, llm, baseline; standart threshold 1.0.
