"""Qabul tekshiruvi: .claude/settings.json README dagi talablarni bajaradimi?

Ishga tushirish: python tekshir.py
Oxirida "Jami: 9/9 OK" chiqishi kerak. Qarorlarni ruxsat.py simulyatori
chiqaradi (Manual rejim). Bu faylni va ruxsat.py ni o'zgartirmang.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from ruxsat import Qoidalar, parse_rule  # noqa: E402

YOL = os.path.join(HERE, ".claude", "settings.json")
natijalar = []
NOM = {"allow": "so'rovsiz", "ask": "so'raladi", "deny": "taqiqlangan"}


def check(nom, ok, tafsilot=""):
    natijalar.append(ok)
    print(f"[{'OK' if ok else 'XATO'}] {nom}")
    if not ok and tafsilot:
        for q in tafsilot.splitlines():
            print("       " + q)


def stsenariy(q, holatlar):
    xato = []
    for tool, arg, kutilgan in holatlar:
        bor = q.qaror(tool, arg)
        if bor != kutilgan:
            xato.append(f"{tool}({arg}) -> {NOM[bor]}, kerak: {NOM[kutilgan]}")
    return not xato, "\n".join(xato[:4]) + (f"\n... yana {len(xato) - 4} ta" if len(xato) > 4 else "")


KENG_BASH = re.compile(r"^\s*(\*|(python[\d.]*|node|ruby|perl|php|sh|bash|zsh|pwsh|deno|bun|npx|uv)\s*(\*|:\*))\s*$")
KENG_EDIT = {"*", "**", "./**", "/**", "//**", "~/**"}


def keng_ruxsatlar(settings):
    p = settings.get("permissions", {})
    yomon = []
    for r in p.get("allow", []):
        tool, spec = parse_rule(r)
        if tool == "Bash" and (spec is None or KENG_BASH.match(spec)):
            yomon.append(r)
        if tool in ("Edit", "Write", "Read") and (spec is None or spec.strip() in KENG_EDIT):
            if tool != "Read":
                yomon.append(r)
    mode = p.get("defaultMode")
    if mode in ("auto", "bypassPermissions"):
        yomon.append(f'defaultMode: "{mode}" (loyiha faylida ishlamaydi va xavfli)')
    return not yomon, "keng yoki xavfli: " + ", ".join(yomon)


def main():
    try:
        with open(YOL, encoding="utf-8") as f:
            settings = json.load(f)
        p = settings["permissions"]
        assert isinstance(p, dict)
        for k in ("allow", "ask", "deny"):
            assert all(isinstance(x, str) for x in p.get(k, [])), f"{k} — satrlar ro'yxati bo'lishi kerak"
        check(".claude/settings.json to'g'ri JSON va permissions bor", True)
    except Exception as e:  # noqa: BLE001
        check(".claude/settings.json to'g'ri JSON va permissions bor", False, f"{type(e).__name__}: {e}")
        print("\nJami: 0/9 OK")
        return 1

    q = Qoidalar(settings)
    ok, t = keng_ruxsatlar(settings)
    check("Keng ruxsatlar va xavfli defaultMode yo'q", ok, t)

    check("1-2. Testlar va lint so'rovsiz, boshqa Python buyruqlari — yo'q", *stsenariy(q, [
        ("Bash", "python -m unittest", "allow"),
        ("Bash", "python -m unittest -v", "allow"),
        ("Bash", "python -m unittest discover -s tests", "allow"),
        ("Bash", "ruff check .", "allow"),
        ("Bash", "ruff check src --fix", "allow"),
        ("Bash", "python -m unittest && ruff check .", "allow"),
        ("Bash", "python -c \"import os; os.remove('x')\"", "ask"),
        ("Bash", "python manage.py flush", "ask"),
        ("Bash", "pip install requests", "ask"),
    ]))

    check("3. Git: o'qish erkin, commit so'raladi, push taqiqlangan", *stsenariy(q, [
        ("Bash", "git status", "allow"),
        ("Bash", "git diff --stat", "allow"),
        ("Bash", "git log --oneline -5", "allow"),
        ("Bash", "git commit -m \"tuzatish\"", "ask"),
        ("Bash", "git commit", "ask"),
        ("Bash", "git push", "deny"),
        ("Bash", "git push --force origin main", "deny"),
        ("Bash", "timeout 60 git push origin main", "deny"),
        ("Bash", "python -m unittest && git push", "deny"),
        ("Bash", "git reset --hard HEAD~3", "ask"),
    ]))

    check("4. Sirlar: .env va secrets/ — o'qish ham, tahrir ham yo'q", *stsenariy(q, [
        ("Read", ".env", "deny"),
        ("Read", "config/.env", "deny"),
        ("Read", "secrets/kalit.pem", "deny"),
        ("Read", "secrets/eski/ichki.key", "deny"),
        ("Edit", ".env", "deny"),
        ("Write", "secrets/yangi.pem", "deny"),
        ("Bash", "cat .env", "deny"),
        ("Bash", "head -5 secrets/kalit.pem", "deny"),
        ("Read", "src/app.py", "allow"),
        ("Bash", "cat src/app.py", "allow"),
    ]))

    check("5. Xavfli buyruqlar: rm -rf va deploy taqiqlangan", *stsenariy(q, [
        ("Bash", "rm -rf build", "deny"),
        ("Bash", "rm -rf /", "deny"),
        ("Bash", "python -m unittest && rm -rf .git", "deny"),
        ("Bash", "./deploy.sh", "deny"),
        ("Bash", "./deploy.sh prod", "deny"),
        ("Bash", "rm eski.txt", "ask"),
    ]))

    check("6. Kod: src/ va tests/ erkin, migrations/ har doim so'raladi", *stsenariy(q, [
        ("Edit", "src/app.py", "allow"),
        ("Write", "src/yangi_modul.py", "allow"),
        ("Edit", "tests/test_app.py", "allow"),
        ("Edit", "migrations/0001_boshlangich.py", "ask"),
        ("Write", "migrations/0002_yangi.py", "ask"),
        ("Edit", "README.md", "ask"),
        ("Edit", "deploy.sh", "ask"),
    ]))

    check("7. Veb: docs.python.org erkin, pastebin.com taqiqlangan", *stsenariy(q, [
        ("WebFetch", "https://docs.python.org/3/library/unittest.html", "allow"),
        ("WebFetch", "https://pastebin.com/raw/abc", "deny"),
        ("WebFetch", "https://example.com", "ask"),
        ("WebFetch", "https://docs.python.org.evil.com/x", "ask"),
    ]))

    # Ro'yxatlar darajalar orasida birlashadi (hujjat: "combines the lists").
    # Hamkasbingiz ~/.claude/settings.json da keng allow qo'ygan bo'lsa ham,
    # loyihaning ask va deny qoidalari ishlashi kerak.
    birlashgan = json.loads(json.dumps(settings))
    birlashgan["permissions"].setdefault("allow", []).extend(["Bash(git *)", "Edit(./**)"])
    check("8. Foydalanuvchining keng allow'i bilan birlashganda ham qoidalar turadi", *stsenariy(Qoidalar(birlashgan), [
        ("Bash", "git commit -m x", "ask"),
        ("Bash", "git push origin main", "deny"),
        ("Edit", "migrations/0002_yangi.py", "ask"),
        ("Edit", ".env", "deny"),
        ("Edit", "src/app.py", "allow"),
    ]))

    print("\nMa'lumot uchun (baholanmaydi) — Bash qoidalari xavfsizlik chegarasi EMAS:")
    for tool, arg in [("Bash", "git -C . push"), ("Bash", "sh deploy.sh"),
                      ("Bash", "grep -r PAYMENT_SECRET ."),
                      ("Bash", "python -c \"print(open('.env').read())\"")]:
        print(f"  {tool}({arg}) -> {NOM[q.qaror(tool, arg)]}")

    print(f"\nJami: {sum(natijalar)}/{len(natijalar)} OK")
    return 0 if all(natijalar) else 1


if __name__ == "__main__":
    sys.exit(main())
