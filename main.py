import logging
import math
import sys
from pathlib import Path

from PIL import Image


class Color:
    r: int = 0
    g: int = 0
    b: int = 0
    a: int = 0

    def __init__(self, r: int, g: int, b: int, a: int):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __str__(self):
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"

    def as_tuple(self) -> tuple:
        return self.r, self.g, self.b


COLOR_TO_CIRCLE = 1 / 255 * 2 * math.pi


def step(x: float) -> float:
    if x < -0.5:
        return -1
    elif x > 0.5:
        return 1
    else:
        return 0


def load_image(path: str or Path) -> Image:
    image = Image.open(str(path))
    return image


def dct_slice(image: Image, x: int, y: int, **kwargs) -> Color:
    size = kwargs.get("size", None)
    if size is None:
        logging.warning("No size given, using 3x3")
        size = (3, 3)
    max_size = kwargs.get("max_size", None)
    r, g, b, a = 0, 0, 0, 0
    count = 0
    for px in range(x, x + size[0]):
        for py in range(y, y + size[1]):
            if px >= max_size[0] or py >= max_size[1]:
                continue
            pixel = image.getpixel((px, py))
            red = step(math.cos(COLOR_TO_CIRCLE * pixel[0]))
            green = step(math.cos(COLOR_TO_CIRCLE * pixel[1]))
            blue = step(math.cos(COLOR_TO_CIRCLE * pixel[2]))

            r += red
            g += green
            b += blue
            count += 1

    r /= count
    g /= count
    b /= count

    r_new = int(math.acos(r) / COLOR_TO_CIRCLE)
    g_new = int(math.acos(g) / COLOR_TO_CIRCLE)
    b_new = int(math.acos(b) / COLOR_TO_CIRCLE)

    return Color(r_new, g_new, b_new, 255)


def create_new_image(scale_down, new_size, orig_size) -> Image:

    window_size = (3, 3)
    w = window_size[0]
    h = window_size[1]
    if scale_down:
        new_img = Image.new("RGB", new_size)
    else:
        new_img = Image.new("RGB", (new_size[0] * w, new_size[1] * h))

    for x in range(0, new_size[0]):
        for y in range(0, new_size[1]):
            pixel_color = dct_slice(img, x * w, y * h, size=window_size, max_size=orig_size).as_tuple()
            if scale_down:
                new_img.putpixel((x, y), pixel_color)
            else:
                for i in range(0, 3):
                    for j in range(0, 3):
                        if x * 3 + i >= orig_size[0] or y * 3 + j >= orig_size[1]:
                            continue
                        new_img.putpixel((x * 3 + i, y * 3 + j), pixel_color)
    return new_img


if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "test_image_original.png"
    path = Path(path)
    for scale_down in [True, False]:
        img = load_image(path)
        orig_size = img.size
        new_size = (orig_size[0] // 3, orig_size[1] // 3)
        new_img = create_new_image(scale_down, new_size, orig_size)
        out_path = path.parent / (path.stem + ("_scale_down" if scale_down else "") + "_dct.png")
        new_img.save(out_path)


