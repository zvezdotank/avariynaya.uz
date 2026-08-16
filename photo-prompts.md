# Промпты для картинок — под веб-интерфейс

Восемь готовых блоков. Каждый копируется целиком и вставляется отдельным
запросом — стиль прописан внутри каждого, чтобы не зависеть от того, помнит
ли чат предыдущее сообщение.

Направление — дуотон: реальная сцена, перекрашенная в два цвета сайта
(`#121110` и `#F5AE39`), с зерном и полутоновой сеткой как в газетной печати.
Фотореализм тут не нужен, от него и была унылость.

## Как работать в вебе

- Генерировать по одному кадру, не списком: на списке модель мешает сюжеты.
- Соотношение сторон вписано в текст словами. Если выдаёт квадрат — попроси
  отдельно: «сделай то же самое в пропорции 4:5» — или обрежь потом сам.
- Если картинка выходит цветной, ответь в тот же чат: «строго два цвета,
  чёрный #121110 и янтарный #F5AE39, никаких синих и зелёных оттенков».
- Скачивать в PNG, складывать в папку `img/` рядом с `index.html`.

---

## 1. Первый экран, главное фото · 4:3

```
High-contrast duotone image, horizontal 4:3. Two colours only: near-black
#121110 in the shadows and warm amber #F5AE39 in the highlights, with a thin
band of pale #F2EFE9 at the very brightest edge. Crushed blacks, blown
highlights, no grey midtones. Coarse film grain and a visible halftone dot
pattern like a screenprinted poster.
Subject: a utility technician in work uniform and heavy gloves standing beside
a service van, arms relaxed, calm competent posture, looking slightly
off-camera. Hard rim light along one shoulder, face half in shadow.
No text, no letters, no logos.
```

## 2. Машина гидродинамики · 16:10

```
High-contrast duotone image, horizontal 16:10. Two colours only: near-black
#121110 in the shadows and warm amber #F5AE39 in the highlights. Crushed
blacks, blown highlights, no grey midtones. Coarse film grain and a visible
halftone dot pattern like a screenprinted poster.
Subject: a sewer jetting truck in a narrow courtyard at night, seen from a low
angle so it reads large. The high-pressure hose reel and pump unit on the truck
bed are clearly readable. Beacon light on the cab as the brightest point.
No text, no letters, no logos.
```

## 3. Камера для диагностики · 16:10

```
High-contrast duotone image, horizontal 16:10. Two colours only: near-black
#121110 in the shadows and warm amber #F5AE39 in the highlights. Crushed
blacks, blown highlights, no grey midtones. Coarse film grain and a visible
halftone dot pattern like a screenprinted poster.
Subject: close-up of a pipe inspection camera reel and its small monitor on a
concrete floor, a gloved hand feeding the cable into an open floor cleanout.
The monitor glow is the brightest point in the frame, everything else falls
into black. No text, no letters, no logos.
```

## 4. Промывка наружной линии во дворе · 16:9

Широкий кадр, идёт через всю галерею.

```
High-contrast duotone image, wide 16:9. Two colours only: near-black #121110
in the shadows and warm amber #F5AE39 in the highlights. Crushed blacks, blown
highlights, no grey midtones. Coarse film grain and a visible halftone dot
pattern like a screenprinted poster.
Subject: two technicians working over an open manhole in a private courtyard,
one feeding a high-pressure hose into the hole, the other reading a pressure
gauge. Steam and fine water mist catching hard side light. A grapevine canopy
and a low brick wall behind them. No text, no letters, no logos.
```

## 5. Труба до и после · 4:5

Самый важный кадр: он работает как доказательство.

```
High-contrast duotone image, vertical 4:5. Two colours only: near-black
#121110 in the shadows and warm amber #F5AE39 in the highlights. Crushed
blacks, blown highlights, no grey midtones. Coarse film grain and a visible
halftone dot pattern like a screenprinted poster.
Subject: two cast iron pipe sections lying side by side on a workbench, shot
from directly above. The left one is heavily caked with hardened scale
narrowing the opening to a third of its diameter; the right one is clean down
to bare metal at full diameter. Hard raking light from one side making the
texture readable. Clinical and evidential, not disgusting.
No text, no letters, no logos.
```

## 6. Откачка септика · 4:5

```
High-contrast duotone image, vertical 4:5. Two colours only: near-black
#121110 in the shadows and warm amber #F5AE39 in the highlights. Crushed
blacks, blown highlights, no grey midtones. Coarse film grain and a visible
halftone dot pattern like a screenprinted poster.
Subject: a vacuum tanker truck with a thick suction hose running into a septic
tank hatch in a yard, the operator guiding the hose, seen from behind. Low sun,
long shadows, dust in the air. Orderly, nothing spilled.
No text, no letters, no logos.
```

## 7. Чистка жироуловителя в кафе · 4:5

```
High-contrast duotone image, vertical 4:5. Two colours only: near-black
#121110 in the shadows and warm amber #F5AE39 in the highlights. Crushed
blacks, blown highlights, no grey midtones. Coarse film grain and a visible
halftone dot pattern like a screenprinted poster.
Subject: a technician kneeling beside an open stainless steel grease trap in a
commercial kitchen after hours. Stainless surfaces and tiled walls catching a
single overhead lamp, the rest of the room falling to black. Tools laid out
neatly on a cloth. Methodical, unhurried mood.
No text, no letters, no logos.
```

## 8. Бригада на выезде ночью · 4:5

```
High-contrast duotone image, vertical 4:5. Two colours only: near-black
#121110 in the shadows and warm amber #F5AE39 in the highlights. Crushed
blacks, blown highlights, no grey midtones. Coarse film grain and a visible
halftone dot pattern like a screenprinted poster.
Subject: two technicians unloading equipment from the back of a service van at
night outside an apartment block, seen from a low angle. Beacon light on the
van roof and headlights cutting through light fog. Urgency without chaos.
No text, no letters, no logos.
```

---

## Что генерировать не надо

**Карта зоны выезда.** Модель нарисует несуществующие районы Ташкента.
Рисовать руками: тёмная схема города, районы разными оттенками чёрного,
зона выезда обведена янтарным, подписи тем же Barlow Condensed.

**Картинка для соцсетей 1200×630.** Буквы модель испортит всегда. Собрать
вручную: кадр №1 плюс чёрная плашка с «Аварийная» и номером телефона.

## Про честность

Как атмосфера дуотон вопросов не вызывает — он и читается как оформление,
а не как репортаж. Но подписывать эти кадры «наши мастера» и «наша техника»
нельзя. Кадр №5 особенно: труба до и после — это обещание результата,
и оно должно быть снято на реальном выезде.
