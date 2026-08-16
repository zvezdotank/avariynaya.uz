# Промпты для картинок

Первый заход был документальной фотографией — получилось уныло и мимо палитры.
Фотореализм здесь и не нужен: сайт чёрно-янтарный, жёсткий, и картинки должны
быть частью этого, а не отдельными снимками внутри него.

Ниже три направления. Рабочая палитра во всех: фон `#121110`, акцент `#F5AE39`,
светлый `#F2EFE9`.

---

## Направление Б — дуотон (рекомендую)

Настоящая сцена, но перекрашенная в два цвета сайта, с крупным зерном и
полутоновой сеткой, как в газетной печати. Даёт документальность — видно
реальную работу, реальных людей — и при этом картинка целиком в палитре.
Единственное из трёх, что одинаково хорошо работает и на людях, и на технике.

**Общий префикс:**

```
High-contrast DUOTONE image, two colours only: near-black #121110 for shadows
and warm amber #F5AE39 for highlights, with a thin band of pale #F2EFE9 in the
brightest areas. Crushed blacks, blown highlights, no midtone mush. Visible
coarse film grain and a subtle halftone dot pattern like newsprint or a
screenprinted poster. Strong single-source side light. Confident, graphic,
poster-like. No text, no letters, no logos, no watermark.
```

**Кадры** (дописывать после префикса):

1. Первый экран, 4:3 — `Mid-shot of a utility technician in work uniform and heavy gloves standing beside a service van, arms relaxed, calm competent posture, looking slightly off-camera. Rim light along one shoulder, face half in shadow.`
2. Машина гидродинамики, 16:10 — `A jetting truck in a narrow courtyard at night, high-pressure hose reel and pump unit clearly readable on the truck bed, beacon light on the cab. Low angle so the truck reads large.`
3. Камера диагностики, 16:10 — `Close-up of a pipe inspection camera reel and its monitor on a concrete floor, a gloved hand feeding the cable into an open floor cleanout. Screen glow as the brightest point in frame.`
4. Промывка во дворе, 16:9 — `Two technicians over an open manhole in a courtyard, one feeding a pressure hose, the other reading a gauge. Steam and water mist catching the side light. Grapevine canopy and low brick wall behind.`
5. Труба до и после, 4:5 — `Two pipe sections side by side shot from directly above: one heavily caked with scale narrowing the bore to a third, one clean to bare metal. Hard raking light making the texture readable. Clinical and evidential.`
6. Откачка септика, 4:5 — `Vacuum tanker with a thick suction hose running into a septic hatch in a yard, operator guiding the hose, seen from behind. Long shadows, dust in the air.`
7. Жироуловитель в кафе, 4:5 — `Technician kneeling by an open stainless steel grease trap in a commercial kitchen after hours. Stainless and tile reflecting one overhead lamp, the rest of the room black. Tools laid out on a cloth.`
8. Бригада ночью, 4:5 — `Two technicians unloading equipment from a service van at night outside an apartment block, beacon light on the roof, headlights cutting through fog. Low angle.`

**Негативный промпт для всех:**

```
full colour, blue tones, green tones, muted grey, flat lighting, stock photo
look, smiling model, 3d render, cartoon, watermark, text, distorted hands,
extra fingers, plastic skin
```

---

## Направление А — плоский вектор, технический постер

Два цвета, толстые уверенные формы, много воздуха, ноль градиентов. Выглядит
как фирменный стиль, а не как иллюстрация. Сильно для техники и оборудования,
слабо для людей: лица в векторе почти всегда выглядят дёшево — если брать это
направление, людей заменить силуэтами или вообще убрать.

```
Bold flat vector poster illustration, strictly two colours: deep near-black
#121110 background and amber #F5AE39 subject, plus one darker amber tone for
shading only. Heavy confident shapes, no gradients, no thin lines, generous
negative space, geometric construction. Diagonal hazard-stripe band of amber
and black across one corner. Swiss graphic design, industrial safety-manual
aesthetic, screenprint feel. No text, no letters, no logos.
```

Дальше сюжет: `a sewer jetting truck at a low three-quarter angle with the
high-pressure hose coiling toward the viewer` и так далее по списку кадров выше.

---

## Направление В — изометрическая схема

Разрез: дом, двор, труба под землёй, колодец, машина наверху. Два цвета плюс
тонкие технические линии. Это не украшение — это объяснение услуги, поэтому
лучше всего ложится на блок «как проходит вызов» и на карту зоны выезда.

```
Isometric technical cutaway diagram, two colours only: #121110 background and
#F5AE39 line work, with #F2EFE9 for the few most important elements. Thin
precise engineering lines, cross-hatched soil layer, clean geometry, blueprint
logic but warm amber instead of blue. Flat, no perspective distortion,
no shading. No text, no labels, no numbers.
```

Сюжет: `a private house with the sewer line running under the courtyard to a
manhole, a service truck parked at the street with a hose running to the
manhole, the blocked section highlighted`.

---

## Карта зоны выезда

Генерировать не стоит — модель нарисует бессмысленную географию с несуществующими
районами. Рисовать руками: тёмная схема Ташкента, районы залиты разными оттенками
чёрного, зона выезда обведена янтарным, подписи районов тем же Barlow Condensed.

## Картинка для соцсетей, 1200×630

Текст моделью не генерировать — буквы поедут. Собрать: кадр из направления Б,
поверх чёрная плашка с «Аварийная» и номером в Barlow Condensed.

---

## Про честность подписей

Это сгенерированные картинки. Пока они стоят как атмосфера — вопросов нет,
дуотон и сам по себе читается как оформление, а не как репортаж. Но подписывать
их «наши мастера» и «наша техника» нельзя, а кадр №5 «труба до и после» вообще
работает как доказательство результата — его надо снять по-настоящему, иначе
это обещание, за которым ничего нет.
