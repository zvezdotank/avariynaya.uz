# Промпты для съёмки/генерации картинок

На странице девять заглушек. Ниже — что должно быть на каждой и промпт для
Gemini. Промпты на английском: модели на нём стабильнее держат детали.

**Общий префикс.** Ставить в начало каждого промпта, иначе картинки не сложатся
в один комплект:

```
Documentary photograph, Tashkent Uzbekistan, utility emergency service.
Dark moody scene, deep charcoal shadows, single warm amber light source
(2700K) as the accent — same amber as a hazard stripe. Muted desaturated
palette apart from that amber. Realistic working conditions, slightly gritty,
no stock-photo gloss, no smiling models, no lens flare, no text or logos.
Shot on 35mm, shallow depth of field, natural grain.
```

**Общий негативный промпт:**

```
cartoon, 3d render, illustration, watermark, text, logo, distorted hands,
extra fingers, plastic skin, oversaturated, clean studio background,
smiling stock model, sewage visibly splashing, gore
```

---

## 1. Первый экран, главное фото — 4:3

Опрятный мастер у машины: чистая форма, перчатки. Задача кадра — снять
брезгливость: человек, которого не страшно пустить в дом.

```
Mid-shot portrait of a male utility technician in his 30s standing beside
a service van at dusk. Clean dark work uniform with amber reflective stripes,
heavy nitrile gloves, calm competent expression, looking slightly off-camera.
Van door open behind him, coiled hoses visible but tidy. Residential Tashkent
street, low warm streetlight. Emphasis on cleanliness and professionalism.
```

## 2. Машина гидродинамики — 16:10

```
A jetting truck parked in a narrow courtyard at night. High-pressure hose reel
and pump unit clearly visible on the truck bed, amber beacon light on the cab
casting warm glow on nearby walls. Wet asphalt reflecting the light. Wide
angle, no people in frame.
```

## 3. Камера для диагностики — 16:10

```
Close-up of a pipe inspection camera reel and its small monitor resting on
a concrete floor, screen showing a grainy greenish view of a pipe interior.
Technician's gloved hand feeding the cable into an open floor cleanout.
Amber worklight from the left, everything else in shadow.
```

## 4. Промывка наружной линии во дворе — 16:9

Широкая, идёт через всю галерею.

```
Wide shot of two technicians working over an open sewer manhole in a private
courtyard. One feeds a high-pressure hose into the hole, the other watches the
pressure gauge. Steam and fine water mist in the cold air, lit from the side
by an amber portable worklight. Grapevine canopy and a low brick wall in the
background, typical Tashkent private house. Evening.
```

## 5. Труба до и после — 4:5

```
Two cast iron pipe sections side by side on a workbench, shot from directly
above. Left one heavily caked with dark grease and mineral scale narrowing
the opening to a third; right one clean down to bare metal, full diameter.
Hard amber side light making the texture readable. Clinical, evidential,
not disgusting.
```

## 6. Откачка септика — 4:5

```
Vacuum tanker truck with a thick suction hose running into a septic tank
hatch in a private yard. Operator in gloves and boots guiding the hose,
seen from behind. Late afternoon, long shadows, dust in the air.
Clean and orderly, no visible spillage.
```

## 7. Чистка жироуловителя в кафе — 4:5

```
Technician kneeling beside an open stainless steel grease trap in a
commercial kitchen, after hours. Stainless surfaces and tiled walls reflecting
a single warm overhead lamp, rest of the kitchen dark. Tools laid out neatly
on a cloth. Focused, methodical mood.
```

## 8. Бригада на выезде ночью — 4:5

```
Two technicians unloading equipment from the back of a service van at night
outside an apartment block. Amber beacon on the van roof, headlights cutting
through light fog. Seen from a low angle so the van reads large. Sense of
urgency without chaos.
```

## 9. Карта зоны выезда — примерно 4:3

Это не фотография. Лучше не генерировать, а нарисовать:
тёмная схема Ташкента, районы залиты по-разному, подписи районов
теми же шрифтами Barlow. Если всё-таки генерировать:

```
Minimal dark map illustration of a city district layout, abstract, no text.
Charcoal background, districts as slightly different dark tones separated by
thin lines, one central zone highlighted in warm amber. Flat vector look,
top-down. No labels, no country shapes, no compass.
```

## 10. Картинка для соцсетей `og:image` — 1200×630

Нужна для превью ссылки в Telegram и WhatsApp. Проще собрать из фото №1
плюс подпись «Аварийная · +998 33 794-70-30» в Barlow Condensed на чёрной
плашке — генерировать текст моделью не стоит, буквы поедут.

---

## Важно

Всё это — сгенерированные картинки, а не съёмка. Подписывать их на живом
сайте как «наши мастера», «наша техника», «наши работы» некорректно: это
фотографии несуществующей бригады. Для запуска сойдёт как временная замена
заглушкам, но фото своей бригады и своих машин надо снять — на такой услуге
доверие держится именно на них. Кадр №5 (труба до и после) особенно: это
доказательство работы, и оно должно быть настоящим.
