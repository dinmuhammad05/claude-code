import unittest

from src.app import buyurtma_summasi


class AppTest(unittest.TestCase):
    def test_summa(self):
        self.assertEqual(buyurtma_summasi([(1000, 2), (500, 1)]), 2500)
