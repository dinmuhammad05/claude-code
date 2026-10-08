# Amaliyot: eslatma — birinchi haqiqiy sessiya

Claude Code kursi, 2-dars. Faqat Python 3.9+ standart kutubxonasi kerak.

| Fayl | Nima |
| --- | --- |
| `eslatma.py` | Terminal uchun kichik eslatmalar daftari: `qosh`, `royxat`, `bajar` |
| `test_eslatma.py` | Mavjud funksiyalar testlari. O‘zgartirmang |
| `muhit.py` | Muhit tekshiruvi: Python, git, claude, API kalit tuzog‘i |
| `tekshir.py` | Qabul tekshiruvi (8 ta). O‘zgartirmang |

```bash
python eslatma.py qosh "Sut olish" --teg uy
python eslatma.py royxat
python eslatma.py bajar 1
```

## Qoidalar: yangi `qidir` funksiyasi

Siz (Claude bilan) `eslatma.py` ga **`qidir(eslatmalar, soz, hammasi=False)`**
funksiyasini va **`qidir`** buyrug‘ini qo‘shasiz.

1. `soz` chetidagi bo‘sh joylarsiz olinadi. Bo‘sh so‘rov (`""`, `"   "`,
   `"#"`) — `ValueError`.
2. Oddiy so‘rov eslatma **matni ichidan** qidiriladi, katta-kichik harf
   farqlanmaydi: `"sut"` → “Sut olish”, “SUTli choy”.
3. `#` bilan boshlangan so‘rov **teg** bo‘yicha qidiradi va teg **aynan**
   mos kelishi kerak (katta-kichik harf farqlanmaydi): `"#ish"` → `ish`
   tegli eslatmalar; `"#is"` → hech narsa.
4. Standart holatda faqat **bajarilmagan** eslatmalar; `hammasi=True` —
   bajarilganlar ham.
5. Natija `id` bo‘yicha o‘sish tartibida.
6. Buyruq: `python eslatma.py qidir <soz> [--hammasi]` — har topilgan
   eslatma `royxat` dagi ko‘rinishda bitta qatorda chiqadi. Hech narsa
   topilmasa — aynan `Hech narsa topilmadi`.

## Topshiriqlar

### 1-daraja: o‘rnatish va muhit

Claude Code’ni darsdagi buyruq bilan o‘rnating, keyin:

```bash
claude --version
claude doctor
python muhit.py
```

`muhit.py` da `XATO` qolmasligi kerak. `OGOH` bo‘lsa — sababini darsdagi
“Muammolar” bo‘limidan toping.

### 2-daraja: birinchi sessiya

```bash
git init && git add . && git commit -m "boshlang'ich holat"
claude --permission-mode default   # Manual rejim: har harakat so‘raladi
```

Sessiyada: loyiha haqida uchta savol bering (darsdagi misollar), bittasida
`@eslatma.py` bilan faylni ko‘rsating; `!python -m unittest` bilan testni
o‘zingiz ishga tushiring; `/status` ga qarang.

### 3-daraja: /init va CLAUDE.md

`/init` ni ishga tushiring. Natijani o‘qing: noto‘g‘ri yoki keraksiz
qatorlarni o‘chiring, test buyrug‘i borligini tekshiring. CLAUDE.md 80
qatordan oshmasin. Commit qiling.

### 4-daraja: birinchi funksiya

“Qoidalar” bo‘limidagi `qidir` ni Claude bilan qo‘shing. Vazifada qoidalar
qayerdaligini, “tayyor” sharti (`python tekshir.py` — `Jami: 8/8 OK`) va
nimaga tegmaslikni yozing. Oxirida Claude’dan o‘zgarishlarni **tavsifli
xabar bilan commit qilishni** so‘rang.

## Tekshiruv mezoni

`python tekshir.py` oxirida `Jami: 8/8 OK`.
