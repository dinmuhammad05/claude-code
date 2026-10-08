"""Ko'rinadigan testlar. Ishga tushirish: python -m unittest -v"""

import unittest

from kassa import chek, qator_summasi


def m(nom, narx, soni, aksiya=False):
    return {"nom": nom, "narx": narx, "soni": soni, "aksiya": aksiya}


class QatorTest(unittest.TestCase):
    def test_oddiy_qator(self):
        self.assertEqual(qator_summasi(12_000, 3), 36_000)

    def test_aksiya_3_ga_2(self):
        # 7 dona: 2 tasi bepul (7 // 3), 5 tasi pullik
        self.assertEqual(qator_summasi(10_000, 7, aksiya=True), 50_000)


class ChekTest(unittest.TestCase):
    def test_promokodsiz(self):
        r = chek([m("non", 4_000, 2), m("sut", 11_000, 1)])
        self.assertEqual(r["oraliq"], 19_000)
        self.assertEqual(r["chegirma"], 0)
        self.assertEqual(r["jami"], 19_000)

    def test_kichik_chegirma(self):
        r = chek([m("choy", 30_000, 2)], promokod="CHEGIRMA10")
        self.assertEqual(r["chegirma"], 6_000)
        self.assertEqual(r["jami"], 54_000)

    def test_chegirma_chegarasi(self):
        # 10% = 120 000, lekin chegirma 50 000 dan oshmaydi
        r = chek([m("televizor", 1_200_000, 1)], promokod="CHEGIRMA10")
        self.assertEqual(r["chegirma"], 50_000)
        self.assertEqual(r["jami"], 1_150_000)

    def test_qqs_narx_ichida(self):
        # Narxlar QQS bilan: 112 000 ning ichidagi 12% QQS = 12 000
        r = chek([m("dazmol", 112_000, 1)])
        self.assertEqual(r["qqs"], 12_000)


if __name__ == "__main__":
    unittest.main()
