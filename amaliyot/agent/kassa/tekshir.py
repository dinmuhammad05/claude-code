"""Qabul tekshiruvi: kod README.md dagi qoidalarni bajaradimi?

Ishga tushirish: python tekshir.py
Oxirida "Jami: 8/8 OK" chiqishi kerak. Bu faylni va test_kassa.py ni
o'zgartirmang — ular "tayyor" nimani anglatishini belgilaydi.
"""

import hashlib
import io
import os
import random
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TEST_HASH = "469cee6b3c49abaaffd53205d4ba65aa07aed3f099a29ca1e7b7ffee14888b28"

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


def yarim_yuqoriga(surat, maxraj):
    """surat / maxraj ni butun songa: 0.5 va undan yuqori — yuqoriga."""
    return (2 * surat + maxraj) // (2 * maxraj)


def m(narx, soni, aksiya=False, nom="x"):
    return {"nom": nom, "narx": narx, "soni": soni, "aksiya": aksiya}


def t_testlar_ozgarmagan():
    with open(os.path.join(HERE, "test_kassa.py"), "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    return h == TEST_HASH, "test_kassa.py o'zgartirilgan — testni emas, kodni tuzating"


def t_korinadigan_testlar():
    import test_kassa

    suite = unittest.defaultTestLoader.loadTestsFromModule(test_kassa)
    out = io.StringIO()
    res = unittest.TextTestRunner(stream=out, verbosity=0).run(suite)
    xatolar = [str(t) for t, _ in res.failures + res.errors]
    return res.wasSuccessful(), "o'tmadi: " + ", ".join(xatolar)


def t_chegirma_yaxlitlash():
    from kassa import chek

    kutilgan = {124: 12, 125: 13, 135: 14, 145: 15, 155: 16}
    for oraliq, ch in kutilgan.items():
        r = chek([m(oraliq, 1)], promokod="CHEGIRMA10")
        if r["chegirma"] != ch:
            return False, f"oraliq {oraliq}: chegirma {r['chegirma']}, kutilgan {ch}"
    return True, ""


def t_qqs_yaxlitlash():
    from kassa import chek

    kutilgan = {14: 2, 42: 5, 100: 11, 19_000: 2_036, 112_000: 12_000}
    for jami, q in kutilgan.items():
        r = chek([m(jami, 1)])
        if r["qqs"] != q:
            return False, f"jami {jami}: qqs {r['qqs']}, kutilgan {q}"
    return True, ""


def t_nomalum_promokod():
    from kassa import chek

    for kod in ["CHEGIRMA20", "chegirma10", ""]:
        try:
            chek([m(10_000, 1)], promokod=kod)
        except ValueError:
            continue
        return False, f"promokod {kod!r} uchun ValueError kutilgan edi"
    r = chek([m(10_000, 1)], promokod=None)
    return r["chegirma"] == 0, "promokod=None — chegirmasiz bo'lishi kerak"


def t_notogri_mahsulot():
    from kassa import chek

    yomonlar = [m(1_000, 0), m(1_000, -2), m(0, 1), m(-500, 1), m(1_000, 2.5), m("1000", 1)]
    for y in yomonlar:
        try:
            chek([m(5_000, 1), y])
        except ValueError:
            continue
        return False, f"narx={y['narx']!r}, soni={y['soni']!r} uchun ValueError kutilgan edi"
    return True, ""


def t_bosh_chek():
    from kassa import chek

    nol = {"oraliq": 0, "chegirma": 0, "jami": 0, "qqs": 0}
    a, b = chek([]), chek([], promokod="CHEGIRMA10")
    return a == nol and b == nol, f"chek([]) = {a}, promokod bilan = {b}"


def t_xossalar():
    from kassa import chek

    rng = random.Random(2026)
    for i in range(300):
        items = [
            m(rng.randint(1, 400_000), rng.randint(1, 9), rng.random() < 0.4)
            for _ in range(rng.randint(1, 6))
        ]
        kod = "CHEGIRMA10" if rng.random() < 0.5 else None
        r = chek(items, promokod=kod)
        oraliq = sum(x["narx"] * (x["soni"] - (x["soni"] // 3 if x["aksiya"] else 0)) for x in items)
        ch = min(yarim_yuqoriga(oraliq * 10, 100), 50_000) if kod else 0
        jami = oraliq - ch
        kut = {"oraliq": oraliq, "chegirma": ch, "jami": jami, "qqs": yarim_yuqoriga(jami * 12, 112)}
        if r != kut:
            return False, f"{i}-chek: {r}, kutilgan {kut}"
    return True, ""


if __name__ == "__main__":
    run("Testlar o'zgartirilmagan", t_testlar_ozgarmagan)
    run("Ko'rinadigan testlar o'tadi", t_korinadigan_testlar)
    run("Chegirma yaxlitlash (0.5 — yuqoriga)", t_chegirma_yaxlitlash)
    run("QQS yaxlitlash (0.5 — yuqoriga)", t_qqs_yaxlitlash)
    run("Noma'lum promokod — ValueError", t_nomalum_promokod)
    run("Noto'g'ri mahsulot — ValueError", t_notogri_mahsulot)
    run("Bo'sh chek", t_bosh_chek)
    run("300 ta tasodifiy chek: qoidalar bajariladi", t_xossalar)
    print(f"\nJami: {sum(natijalar)}/{len(natijalar)} OK")
    sys.exit(0 if all(natijalar) else 1)
