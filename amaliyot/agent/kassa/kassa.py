"""Do'kon kassasi: chek summasini hisoblash.

Qoidalar README.md dagi "Qoidalar" bo'limida. Kod qoidaga mos kelmasa —
qoida to'g'ri, kod xato.
"""

PROMOKODLAR = {"CHEGIRMA10": 10}
CHEGIRMA_CHEGARASI = 50_000
QQS_FOIZ = 12


def qator_summasi(narx, soni, aksiya=False):
    """Bitta mahsulot qatori: narx x soni, aksiyada har 3 tadan 1 tasi bepul."""
    pullik = soni - soni // 3 if aksiya else soni
    return narx * pullik


def chek(mahsulotlar, promokod=None):
    """Chekni hisoblaydi.

    mahsulotlar: [{"nom": str, "narx": int, "soni": int, "aksiya": bool}, ...]
    Natija: {"oraliq": int, "chegirma": int, "jami": int, "qqs": int}
    """
    oraliq = 0
    for m in mahsulotlar:
        oraliq += qator_summasi(m["narx"], m["soni"], m.get("aksiya", False))

    chegirma = 0
    if promokod in PROMOKODLAR:
        chegirma = round(oraliq * PROMOKODLAR[promokod] / 100)

    jami = oraliq - chegirma
    qqs = round(jami * QQS_FOIZ / 100)
    return {"oraliq": oraliq, "chegirma": chegirma, "jami": jami, "qqs": qqs}
