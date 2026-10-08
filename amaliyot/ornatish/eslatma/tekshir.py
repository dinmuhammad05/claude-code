"""Qabul tekshiruvi: 2-dars amaliyoti tugadimi?

Ishga tushirish: python tekshir.py
Oxirida "Jami: 8/8 OK" chiqishi kerak. Bu faylni va test_eslatma.py ni
o'zgartirmang — ular "tayyor" nimani anglatishini belgilaydi.
"""

import hashlib
import io
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TEST_HASH = "ae6442cc39eee10bea72b265e7ca890706f66282e7e0ddba69c39375a119ae0c"
natijalar = []


def check(nom, ok, tafsilot=""):
    natijalar.append(ok)
    print(f"[{'OK' if ok else 'XATO'}] {nom}")
    if not ok and tafsilot:
        print("       " + tafsilot)


def run(nom, fn):
    try:
        ok, tafsilot = fn()
    except Exception as e:  # noqa: BLE001 — har qanday xato tekshiruvni yiqitadi
        ok, tafsilot = False, f"{type(e).__name__}: {e}"
    check(nom, ok, tafsilot)


def git(*args):
    r = subprocess.run(["git", *args], cwd=HERE, capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or f"git {' '.join(args)} xato")
    return r.stdout


def namuna():
    from eslatma import bajar, qosh

    e = []
    qosh(e, "Sut olish", "uy")              # 1
    qosh(e, "Hisobotni yuborish", "ish")    # 2
    qosh(e, "SUTli choy damlash")           # 3
    qosh(e, "Ishxonaga sut olib borish", "Ish")  # 4
    qosh(e, "Kitob o'qish", "uy")           # 5
    bajar(e, 1)
    return e


def t_testlar_ozgarmagan():
    with open(os.path.join(HERE, "test_eslatma.py"), "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    return h == TEST_HASH, "test_eslatma.py o'zgartirilgan — testni emas, kodni tuzating"


def t_mavjud_testlar():
    import test_eslatma

    suite = unittest.defaultTestLoader.loadTestsFromModule(test_eslatma)
    res = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    xatolar = [str(t) for t, _ in res.failures + res.errors]
    return res.wasSuccessful(), "o'tmadi: " + ", ".join(xatolar)


def t_claude_md():
    yol = os.path.join(HERE, "CLAUDE.md")
    if not os.path.exists(yol):
        return False, "CLAUDE.md yo'q — sessiyada /init ni ishga tushiring"
    with open(yol, encoding="utf-8") as f:
        qatorlar = f.read().splitlines()
    if len(qatorlar) > 80:
        return False, f"CLAUDE.md {len(qatorlar)} qator — 80 tagacha qisqartiring"
    if not any("unittest" in q for q in qatorlar):
        return False, "CLAUDE.md da testlarni ishga tushirish buyrug'i (unittest) yo'q"
    return True, ""


def t_qidir_asosiy():
    from eslatma import qidir

    ids = lambda r: [x.id for x in r]
    if ids(qidir(namuna(), "sut")) != [3, 4]:
        return False, f"qidir(e, 'sut') = {ids(qidir(namuna(), 'sut'))}, kutilgan [3, 4]"
    if ids(qidir(namuna(), "  KITOB ")) != [5]:
        return False, "katta-kichik harf va chetdagi bo'sh joy e'tiborga olinmasligi kerak"
    if ids(qidir(namuna(), "yo'q-narsa")) != []:
        return False, "mos kelmasa — bo'sh ro'yxat"
    return True, ""


def t_qidir_qoidalar():
    from eslatma import qidir

    ids = lambda r: [x.id for x in r]
    if ids(qidir(namuna(), "sut", hammasi=True)) != [1, 3, 4]:
        return False, f"hammasi=True: {ids(qidir(namuna(), 'sut', hammasi=True))}, kutilgan [1, 3, 4]"
    if ids(qidir(namuna(), "#ish")) != [2, 4]:
        return False, f"'#ish' (teg): {ids(qidir(namuna(), '#ish'))}, kutilgan [2, 4]"
    if ids(qidir(namuna(), "#is")) != []:
        return False, "teg bo'yicha qidiruv aniq moslik bo'lishi kerak ('#is' hech narsa topmaydi)"
    if ids(qidir(namuna(), "#UY", hammasi=True)) != [1, 5]:
        return False, "teg qidiruvi ham katta-kichik harfga sezgir bo'lmasligi va hammasi=True ni hisobga olishi kerak"
    for bosh in ["", "   ", "#", " # "]:
        try:
            qidir(namuna(), bosh)
        except ValueError:
            continue
        return False, f"qidir(e, {bosh!r}) uchun ValueError kutilgan edi"
    return True, ""


def t_cli():
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, ESLATMA_FAYL=os.path.join(d, "e.json"))
        cmd = lambda *a: subprocess.run(
            [sys.executable, os.path.join(HERE, "eslatma.py"), *a],
            capture_output=True, text=True, env=env, timeout=30,
        )
        cmd("qosh", "Sut olish", "--teg", "uy")
        cmd("qosh", "Non olish")
        cmd("qosh", "Sutli choy")
        cmd("bajar", "3")
        r = cmd("qidir", "SUT")
        if r.returncode != 0 or r.stdout.strip().splitlines() != ["[ ] 1. Sut olish #uy"]:
            return False, f"'qidir SUT' chiqishi: {r.stdout.strip()!r} (kod {r.returncode})"
        r = cmd("qidir", "sut", "--hammasi")
        if r.stdout.strip().splitlines() != ["[ ] 1. Sut olish #uy", "[x] 3. Sutli choy"]:
            return False, f"'qidir sut --hammasi' chiqishi: {r.stdout.strip()!r}"
        r = cmd("qidir", "olma")
        if r.returncode != 0 or r.stdout.strip() != "Hech narsa topilmadi":
            return False, f"mos kelmasa 'Hech narsa topilmadi' kutilgan, keldi: {r.stdout.strip()!r}"
    return True, ""


def t_git_tarix():
    git("rev-parse", "--is-inside-work-tree")
    commitlar = int(git("rev-list", "--count", "HEAD").strip())
    if commitlar < 2:
        return False, f"{commitlar} ta commit — boshlang'ich commit va Claude bilan qilingan commit kerak"
    ozgargan = git("status", "--porcelain", "--untracked-files=no").strip()
    if ozgargan:
        return False, "commit qilinmagan o'zgarishlar bor:\n       " + ozgargan.replace("\n", "\n       ")
    return True, ""


def t_shaxsiy_fayllar():
    kuzatilgan = git("ls-files").splitlines()
    yomon = [f for f in kuzatilgan if f == "CLAUDE.local.md" or f.endswith("settings.local.json")
             or re.fullmatch(r"eslatmalar\.json", f)]
    return not yomon, "git'ga tushmasligi kerak bo'lgan fayllar: " + ", ".join(yomon)


if __name__ == "__main__":
    run("Testlar o'zgartirilmagan", t_testlar_ozgarmagan)
    run("Mavjud testlar o'tadi", t_mavjud_testlar)
    run("CLAUDE.md bor, qisqa va test buyrug'ini biladi", t_claude_md)
    run("qidir: asosiy qidiruv", t_qidir_asosiy)
    run("qidir: hammasi, teglar, bo'sh so'rov", t_qidir_qoidalar)
    run("CLI: python eslatma.py qidir ...", t_cli)
    run("Git: o'zgarishlar commit qilingan", t_git_tarix)
    run("Git: shaxsiy va ma'lumot fayllari repoda yo'q", t_shaxsiy_fayllar)
    print(f"\nJami: {sum(natijalar)}/{len(natijalar)} OK")
    sys.exit(0 if all(natijalar) else 1)
