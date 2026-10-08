"""Do'kon API: buyurtma summasini hisoblash (amaliyot uchun namuna kod)."""


def buyurtma_summasi(qatorlar):
    return sum(narx * soni for narx, soni in qatorlar)
