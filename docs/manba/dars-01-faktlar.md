# 1-dars uchun tekshirilgan faktlar (2026-10-08)

Manba: rasmiy hujjatlar. Iqtiboslar WebFetch matnidan olingan — nashrdan oldin jonli sahifa bilan solishtiring.

## Agent sikli — https://code.claude.com/docs/en/how-claude-code-works
- "When you give Claude a task, it works through three phases: gather context, take action, and verify results. These phases blend together."
- "A question about your codebase might only need context gathering. A bug fix cycles through all three phases repeatedly."
- "You can interrupt at any point to steer Claude in a different direction, provide additional context, or ask it to try a different approach."
- Esc: "The running tool call is canceled and Claude waits for your next instruction." Enter bilan yozilgan tuzatish navbatga qo'yiladi va joriy asbob chaqiruvlari tugagach o'qiladi.
- Harness: "Claude Code is the layer around the model that provides the tools and manages the context the model sees. This surrounding layer is what the term agentic harness refers to."
- "Without tools, Claude can only respond with text. With tools, Claude can act."
- Kontekst to'lganda: "It clears older tool outputs first, then summarizes the conversation if needed. Your requests and key code snippets are preserved; detailed instructions from early in the conversation may be lost."
- Asbob toifalari: File operations, Search, Execution, Web, Code intelligence (plagin talab qiladi). Orkestratsiya alohida.
- Kontekst tarkibi: "conversation history, file contents, command outputs, CLAUDE.md, auto memory, loaded skills, and system instructions."
- "Sessions are independent. Each new session starts with a fresh context window." Tarix `~/.claude/projects/` ostida JSONL.
- MEMORY.md: birinchi 200 qator yoki 25KB har sessiya boshida yuklanadi.
- Checkpoint: "Before Claude edits a file, it snapshots the current contents." Git'dan alohida.
- "File edits are reversible." / "Actions that affect remote systems (databases, APIs, deployments) can't be checkpointed."
- Manual: "Claude asks before file edits and shell commands." Auto: klassifikator xavfli amallarni bloklaydi.

## Asboblar — https://code.claude.com/docs/en/tools-reference
- Read: ruxsat yo'q. Edit: ruxsat bor; aniq satr almashtirish, oldin o'qish shart. Bash: ruxsat bor; o'qish uchungi buyruqlar so'ralmaydi; har buyruq alohida jarayon, env saqlanmaydi.
- Glob, Grep: "Absent by default on macOS, Linux, and WSL." Bunda qidiruv Bash orqali `find` va `grep` (ichida `bfs` va `ugrep`). Windows'da standart to'plamda.
- WebFetch, WebSearch: ruxsat bor. Agent: subagent, o'z kontekst oynasi bilan.

## Kontekst oynasi — https://code.claude.com/docs/en/context-window
- Illyustratsiya: 200K oyna ("illustrative"). Boshlang'ich yuklama misoli: system prompt 4 200; MEMORY.md 680; muhit 280; MCP (kechiktirilgan) 120; skill tavsiflari 450; ~/.claude/CLAUDE.md 320; loyiha CLAUDE.md 1 800 (jami 7 850).
- Bitta fayl o'qish misoli: 2 400 token. "File reads dominate context usage."
- Compact'dan keyin: CLAUDE.md va auto memory diskdan qayta yuklanadi; oxirgi o'zgargan 5 tagacha fayl qayta o'qiladi.
- Qayta-qayta to'lsa auto-compact bir necha urinishdan keyin to'xtaydi va xato ko'rsatadi.

## Best practices — https://code.claude.com/docs/en/best-practices
- "Give Claude a check it can run: tests, a build, a screenshot to compare. It's the difference between a session you watch and one you walk away from."
- "Without a check it can run, 'looks done' is the only signal available, and you become the verification loop."
- "Have Claude show evidence rather than asserting success."
- "Claude's context window fills up fast, and performance degrades as it fills."
- Xato naqshlari: kitchen sink session; correcting over and over; over-specified CLAUDE.md; trust-then-verify gap; infinite exploration.
- Bash orqali o'zgarishlar checkpoint'ga tushmaydi.

## Narx — https://code.claude.com/docs/en/costs
- "Claude Code charges by API token consumption."
- Korporativ o'rtacha: ~$13 / faol kun, $150–250 / oy; foydalanuvchilarning 90% uchun kuniga $30 dan kam.
- Prompt caching avtomatik. Kesh umri: obunada bir soat, API kalitda standart besh daqiqa.
- `/usage` — taxmin, ro'yxat narxida.

## Klavishalar — https://code.claude.com/docs/en/interactive-mode
- Esc — to'xtatish; Esc Esc (bo'sh kiritishda) — rewind menyusi; Shift+Tab — ruxsat rejimlari; Ctrl+G — promptni muharrirda tahrirlash; `!` — shell rejimi; `@` — fayl yo'lini eslatish.
