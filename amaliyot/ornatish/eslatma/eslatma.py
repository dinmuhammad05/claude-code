"""Eslatma: terminal uchun kichik eslatmalar daftari.

Ishlatish:
    python eslatma.py qosh "Sut olish" --teg uy
    python eslatma.py royxat [--hammasi]
    python eslatma.py bajar 2

Eslatmalar JSON faylda saqlanadi: standart holatda ./eslatmalar.json,
ESLATMA_FAYL muhit o'zgaruvchisi bilan boshqa fayl berish mumkin.
"""

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from typing import List, Optional


@dataclass
class Eslatma:
    id: int
    matn: str
    teg: Optional[str] = None
    bajarilgan: bool = False


def fayl_yoli() -> str:
    return os.environ.get("ESLATMA_FAYL", "eslatmalar.json")


def yukla(yol: str) -> List[Eslatma]:
    if not os.path.exists(yol):
        return []
    with open(yol, encoding="utf-8") as f:
        return [Eslatma(**d) for d in json.load(f)]


def saqla(yol: str, eslatmalar: List[Eslatma]) -> None:
    with open(yol, "w", encoding="utf-8") as f:
        json.dump([asdict(e) for e in eslatmalar], f, ensure_ascii=False, indent=2)


def qosh(eslatmalar: List[Eslatma], matn: str, teg: Optional[str] = None) -> Eslatma:
    matn = matn.strip()
    if not matn:
        raise ValueError("eslatma matni bo'sh bo'lmasligi kerak")
    yangi_id = max((e.id for e in eslatmalar), default=0) + 1
    e = Eslatma(yangi_id, matn, teg.strip().lower() if teg else None)
    eslatmalar.append(e)
    return e


def royxat(eslatmalar: List[Eslatma], hammasi: bool = False) -> List[Eslatma]:
    natija = [e for e in eslatmalar if hammasi or not e.bajarilgan]
    return sorted(natija, key=lambda e: e.id)


def bajar(eslatmalar: List[Eslatma], eslatma_id: int) -> Eslatma:
    for e in eslatmalar:
        if e.id == eslatma_id:
            e.bajarilgan = True
            return e
    raise KeyError(eslatma_id)


def chiroyli(e: Eslatma) -> str:
    belgi = "x" if e.bajarilgan else " "
    teg = f" #{e.teg}" if e.teg else ""
    return f"[{belgi}] {e.id}. {e.matn}{teg}"


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="eslatma")
    sub = p.add_subparsers(dest="buyruq", required=True)
    q = sub.add_parser("qosh")
    q.add_argument("matn")
    q.add_argument("--teg")
    r = sub.add_parser("royxat")
    r.add_argument("--hammasi", action="store_true")
    b = sub.add_parser("bajar")
    b.add_argument("id", type=int)
    args = p.parse_args(argv)

    yol = fayl_yoli()
    eslatmalar = yukla(yol)
    if args.buyruq == "qosh":
        e = qosh(eslatmalar, args.matn, args.teg)
        saqla(yol, eslatmalar)
        print(f"Qo'shildi: {chiroyli(e)}")
    elif args.buyruq == "royxat":
        for e in royxat(eslatmalar, args.hammasi):
            print(chiroyli(e))
    elif args.buyruq == "bajar":
        try:
            e = bajar(eslatmalar, args.id)
        except KeyError:
            print(f"{args.id} raqamli eslatma yo'q", file=sys.stderr)
            return 1
        saqla(yol, eslatmalar)
        print(f"Bajarildi: {chiroyli(e)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
