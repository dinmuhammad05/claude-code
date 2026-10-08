# Amaliyot: kassa — agent siklini o‘z ko‘zingiz bilan ko‘rish

Claude Code kursi, 1-dars. Faqat Python 3.9+ standart kutubxonasi kerak.

| Fayl | Nima |
| --- | --- |
| `kassa.py` | Chek hisoblaydigan kod. **Xatolari bor.** |
| `test_kassa.py` | Ko‘rinadigan testlar. O‘zgartirmang. |
| `tekshir.py` | Qabul tekshiruvi: kod quyidagi qoidalarni bajaradimi. O‘zgartirmang. |
| `JURNAL.md` | Kuzatuvlaringizni shu yerga yozasiz. |

Boshlashdan oldin papkani git repoga aylantiring — har sessiyadan keyin
toza holatga qaytish uchun kerak bo‘ladi:

```bash
git init && git add . && git commit -m "boshlang'ich holat"
```

## Qoidalar

Chek qoidalari shu ro‘yxatdagidek. Kod bilan qoida farq qilsa — qoida to‘g‘ri.

1. Mahsulotda `narx` (so‘m) va `soni` bor. Ikkalasi ham **musbat butun son**
   bo‘lishi shart. Aks holda `chek` funksiyasi `ValueError` ko‘taradi.
2. Qator summasi = `narx × soni`.
3. `aksiya: True` bo‘lgan mahsulotda har 3 donadan 1 tasi bepul: bepul
   donalar soni `soni // 3`.
4. Oraliq summa — barcha qatorlar yig‘indisi.
5. Promokod faqat `CHEGIRMA10`: oraliq summadan 10%, lekin **50 000 so‘mdan
   oshmaydi**. Katta-kichik harf farq qiladi. Boshqa har qanday promokod
   (bo‘sh satr ham) — `ValueError`. Promokod berilmasa (`None`) — chegirma 0.
6. Jami = oraliq − chegirma.
7. Narxlar QQS bilan. Chekda jami ichidagi 12% QQS ko‘rsatiladi:
   `jami × 12 / 112`.
8. Yaxlitlash: chegirma ham, QQS ham butun so‘mga, **0.5 va undan yuqori —
   yuqoriga** (12.5 → 13, 4.5 → 5).
9. Bo‘sh chek xato emas: hammasi 0.

## Topshiriqlar

### 1-daraja: agentdan oldin (10 daqiqa, Claude’siz)

```bash
python -m unittest -v
python tekshir.py
```

`JURNAL.md` ning birinchi bo‘limini to‘ldiring: nechta test yiqildi,
`tekshir.py` nechta xato topdi, agent ishni tugatish uchun qaysi fayllarni
o‘qishi **shart** deb o‘ylaysiz.

### 2-daraja: A sessiya — noaniq vazifa

Claude Code’ni Manual rejimda oching (`claude --permission-mode default`)
va **faqat shuni** yozing:

```text
testlar o'tmayapti, tuzatib ber
```

Har ruxsat so‘rovini o‘qib chiqing. Tugagach, agentga hech narsa demasdan:

```bash
python tekshir.py
git diff --stat
```

Ichida `/context` ni ham yozib ko‘ring. `JURNAL.md` ning A bo‘limini
to‘ldiring. Keyin toza holatga qayting va sessiyadan chiqing:

```bash
git checkout -- .
```

### 3-daraja: B sessiya — tekshiriladigan maqsad

**Yangi** sessiya oching va darsdagi “yaxshi vazifa” shablonidan foydalaning:
qoidalar qayerda, “tayyor” nimani anglatadi (qaysi buyruq qanday natija
berishi kerak), nimaga tegmaslik kerak. B bo‘limini to‘ldiring va A bilan
solishtiring.

### 4-daraja: o‘z tekshiruvingiz

`tekshir.py` ni ochmasdan, `test_meniki.py` faylida bitta test yozing: u
asl `kassa.py` dagi yaxlitlash xatosini ushlasin. Nega `test_kassa.py` bu
xatoni ko‘rmagan — JURNAL’ga bir gap bilan yozing.

## Tekshiruv mezoni

- `python tekshir.py` oxirida `Jami: 8/8 OK`;
- `git diff` da `test_kassa.py` va `tekshir.py` o‘zgarmagan;
- `JURNAL.md` dagi to‘rtta bo‘lim to‘ldirilgan.

Natija har safar bir xil chiqmaydi: model ehtimollikka tayanadi, A sessiya
ba’zan hammasini to‘g‘ri tuzatadi. Mashqning maqsadi — “tayyor”ni **qanday
bilganingizni** ko‘rish: o‘zingiz tekshirdingizmi yoki “tayyor” degan gapga
ishondingizmi.
