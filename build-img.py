#!/usr/bin/env python3
"""Пересобирает img/*.webp из исходников Gemini.

Исходники в репозиторий не кладём — они весят под 40 МБ. Скрипт нужен, чтобы
рецепт обработки не жил только в переписке: если понадобится перегенерировать
картинки или заменить кадр, параметры здесь.

    python3 build-img.py ~/Downloads

Обработка одинаковая для всех: оттенок к фирменному #f5ae39, насыщенность к
0.77, пол чёрного к #121110. Разница только в CUT — насколько жёстко давим
тёмное:

- вырезки (предметы на чёрном) — CUT 52, фон становится плоским и сливается
  со страницей, рамка не нужна;
- сцены (работа на объекте) — CUT 8, поднимаем только пол чёрного, детали
  кладки и листвы остаются, кадр живёт в рамке.
"""
import sys, pathlib, colorsys
from PIL import Image

BG = (0x12, 0x11, 0x10)
HUE = round(37 / 360 * 255)          # фирменный янтарный
QUALITY = 74                          # ниже полутоновая сетка начинает сыпаться

# имя: (файл-исходник, тип, множитель насыщенности, пропорция, ширины)
SHOTS = {
    'hero':    ('Gemini_Generated_Image_7zdpx77zdpx77zdp.jpeg', 'cut',   0.92, None,  (1400, 1100, 800)),
    'jet':     ('Gemini_Generated_Image_7c1sgs7c1sgs7c1s.jpeg', 'cut',   0.92, 16/10, (1200, 800)),
    'cam':     ('Gemini_Generated_Image_v4x55jv4x55jv4x5.jpeg', 'cut',   0.75, 16/10, (1200, 800)),
    'pipe':    ('Gemini_Generated_Image_62q6ee62q6ee62q6.jpeg', 'cut',   0.92, 4/5,   (1200, 800)),
    'yard':    ('Gemini_Generated_Image_l026ycl026ycl026.jpeg', 'scene', 1.20, 16/9,  (1600, 900)),
    'septic':  ('Gemini_Generated_Image_58iv1x58iv1x58iv.jpeg', 'scene', 1.10, 4/5,   (1200, 800)),
    'kitchen': ('Gemini_Generated_Image_4elai34elai34ela.jpeg', 'scene', 1.00, 4/5,   (1200, 800)),
    'night':   ('Gemini_Generated_Image_x0nvukx0nvukx0nv.jpeg', 'scene', 1.30, 4/5,   (1200, 800)),
}


def recolor(im, sat, cut):
    h, s, v = im.convert('HSV').split()
    h = h.point(lambda _: HUE)
    s = s.point(lambda x: min(255, round(x * sat)))
    o = Image.merge('HSV', (h, s, v)).convert('RGB')
    lut = [[round(BG[c] + (0 if i <= cut else (i - cut) * 255 / (255 - cut)) * (255 - BG[c]) / 255)
            for i in range(256)] for c in range(3)]
    r, g, b = o.split()
    return Image.merge('RGB', (r.point(lut[0]), g.point(lut[1]), b.point(lut[2])))


def tighten(o, aspect, margin=0.05):
    """обрезать по краям предмета и добить полями до нужной пропорции"""
    x0, y0, x1, y1 = o.convert('L').point(lambda v: 255 if v > 40 else 0).getbbox()
    W, H = o.size
    mx, my = round((x1 - x0) * margin), round((y1 - y0) * margin)
    c = o.crop((max(0, x0 - mx), max(0, y0 - my), min(W, x1 + mx), min(H, y1 + my)))
    cw, ch = c.size
    tw, th = (cw, round(cw / aspect)) if cw / ch > aspect else (round(ch * aspect), ch)
    canvas = Image.new('RGB', (max(tw, cw), max(th, ch)), BG)
    canvas.paste(c, ((max(tw, cw) - cw) // 2, (max(th, ch) - ch) // 2))
    return canvas


def crop_to(o, aspect):
    """обрезать сцену по центру внутрь кадра, не выходя за границы"""
    w, h = o.size
    tw, th = (round(h * aspect), h) if w / h > aspect else (w, round(w / aspect))
    return o.crop(((w - tw) // 2, (h - th) // 2, (w - tw) // 2 + tw, (h - th) // 2 + th))


def main(srcdir):
    src = pathlib.Path(srcdir)
    out = pathlib.Path('img')
    out.mkdir(exist_ok=True)
    total = 0
    for name, (fn, kind, sat, aspect, widths) in SHOTS.items():
        p = src / fn
        if not p.exists():
            print(f'  {name}: исходник не найден, пропускаю ({fn})')
            continue
        im = Image.open(p).convert('RGB')
        o = recolor(im, sat, 52 if kind == 'cut' else 8)
        if aspect:
            o = tighten(o, aspect) if kind == 'cut' else crop_to(o, aspect)
        for w in widths:
            h = round(w * o.size[1] / o.size[0])
            f = out / f'{name}-{w}.webp'
            o.resize((w, h), Image.LANCZOS).save(f, 'WEBP', quality=QUALITY, method=6)
            total += f.stat().st_size
        print(f'  {name}: {o.size[0]}×{o.size[1]} → {", ".join(str(w) for w in widths)}')
    print(f'итого {total/1024:.0f} КБ')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path.home() / 'Downloads'))
