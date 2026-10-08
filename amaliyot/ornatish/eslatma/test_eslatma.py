"""Mavjud funksiyalar uchun testlar. Ishga tushirish: python -m unittest -v"""

import unittest

from eslatma import Eslatma, bajar, chiroyli, qosh, royxat


class EslatmaTest(unittest.TestCase):
    def setUp(self):
        self.e = []
        qosh(self.e, "Sut olish", "Uy")
        qosh(self.e, "Hisobotni yuborish", "ish")
        qosh(self.e, "Kitob o'qish")

    def test_qosh_id_va_teg(self):
        self.assertEqual([x.id for x in self.e], [1, 2, 3])
        self.assertEqual(self.e[0].teg, "uy")
        self.assertIsNone(self.e[2].teg)

    def test_bosh_matn(self):
        with self.assertRaises(ValueError):
            qosh(self.e, "   ")

    def test_royxat_bajarilganlarsiz(self):
        bajar(self.e, 2)
        self.assertEqual([x.id for x in royxat(self.e)], [1, 3])
        self.assertEqual([x.id for x in royxat(self.e, hammasi=True)], [1, 2, 3])

    def test_bajar_yoq_id(self):
        with self.assertRaises(KeyError):
            bajar(self.e, 99)

    def test_chiroyli(self):
        self.assertEqual(chiroyli(Eslatma(5, "Non", "uy", True)), "[x] 5. Non #uy")


if __name__ == "__main__":
    unittest.main()
