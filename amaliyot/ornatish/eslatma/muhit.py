"""Muhit tekshiruvi: Claude Code ishlashi uchun kerakli narsalar joyidami?

Ishga tushirish: python muhit.py
Hech narsani o'zgartirmaydi — faqat o'qiydi va natijani chiqaradi.
"""

import os
import platform
import shutil
import subprocess
import sys

natija = {"OK": 0, "OGOH": 0, "XATO": 0}


def chiq(daraja, matn, izoh=""):
    natija[daraja] += 1
    print(f"[{daraja}] {matn}")
    if izoh:
        for qator in izoh.splitlines():
            print("       " + qator)


def barcha_nusxalar(nom):
    """PATH dagi barcha `nom` dasturlari (which -a ga o'xshash)."""
    kengaytmalar = [""]
    if os.name == "nt":
        kengaytmalar = os.environ.get("PATHEXT", ".EXE;.CMD;.BAT").lower().split(";")
    topildi = []
    for papka in os.environ.get("PATH", "").split(os.pathsep):
        for k in kengaytmalar:
            yol = os.path.join(papka, nom + k)
            if os.path.isfile(yol) and os.access(yol, os.X_OK):
                haqiqiy = os.path.realpath(yol)
                if haqiqiy not in topildi:
                    topildi.append(haqiqiy)
    return topildi


def versiya(buyruq):
    try:
        r = subprocess.run(buyruq, capture_output=True, text=True, timeout=30)
        return (r.stdout or r.stderr).strip().splitlines()[0] if (r.stdout or r.stderr) else ""
    except (OSError, subprocess.TimeoutExpired) as e:
        return f"ishga tushmadi: {e}"


def main():
    print(f"Tizim: {platform.system()} {platform.release()}\n")

    # Python
    if sys.version_info >= (3, 9):
        chiq("OK", f"Python {platform.python_version()}")
    else:
        chiq("XATO", f"Python {platform.python_version()} — amaliyot uchun 3.9+ kerak")

    # Git
    if shutil.which("git"):
        chiq("OK", versiya(["git", "--version"]))
    else:
        chiq("XATO", "git topilmadi", "Amaliyotdagi commit va diff uchun git kerak.")

    # Claude Code
    nusxalar = barcha_nusxalar("claude")
    if not nusxalar:
        chiq(
            "XATO",
            "claude buyrug'i PATH da topilmadi",
            "O'rnatgan bo'lsangiz — terminalni qayta oching yoki PATH ni tekshiring.\n"
            "VS Code kengaytmasi claude ni PATH ga qo'shmaydi: CLI alohida o'rnatiladi.",
        )
    else:
        chiq("OK", f"claude: {versiya([nusxalar[0], '--version'])}  ({nusxalar[0]})")
        if len(nusxalar) > 1:
            chiq(
                "OGOH",
                f"PATH da {len(nusxalar)} ta claude bor — qaysi biri ishlashi aniq emas",
                "\n".join(nusxalar) + "\nKeraksizini o'chiring (masalan, eski npm o'rnatishni).",
            )

    # API kalit tuzog'i
    if os.environ.get("ANTHROPIC_API_KEY"):
        chiq(
            "OGOH",
            "ANTHROPIC_API_KEY o'rnatilgan",
            "Obunangiz bo'lsa ham, tasdiqlaganingizdan keyin Claude Code shu kalitdan\n"
            "foydalanadi (to'lov API hisobidan). Obuna kerak bo'lsa: unset ANTHROPIC_API_KEY,\n"
            "keyin sessiyada /status bilan tekshiring.",
        )
    else:
        chiq("OK", "ANTHROPIC_API_KEY o'rnatilmagan (obuna bilan kirish ishlatiladi)")

    # Windows va WSL
    if os.name == "nt":
        if shutil.which("bash"):
            chiq("OK", "Windows: Git Bash topildi — Bash asbobi ishlaydi")
        else:
            chiq("OGOH", "Windows: Git for Windows topilmadi", "Bash asbobi o'rniga PowerShell ishlatiladi.")
        chiq("OGOH", "Windows (native): sandbox qo'llab-quvvatlanmaydi", "Sandbox kerak bo'lsa — WSL 2.")
    elif "microsoft" in platform.release().lower():
        chiq("OK", "WSL aniqlandi — Linux o'rnatuvchisidan foydalaning (WSL 2 tavsiya)")

    print(f"\nNatija: {natija['OK']} OK, {natija['OGOH']} ogohlantirish, {natija['XATO']} xato")
    return 1 if natija["XATO"] else 0


if __name__ == "__main__":
    sys.exit(main())
