import os
import numpy as np
import random
from PIL import Image
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype


Color = {"red": (255, 0, 0), "yellow": (255, 255, 0), "blue": (0, 0, 255), "green": (0, 255, 0), "black": (0, 0, 0),
         "white": (255, 255, 255)}


class ImageCaptcha:

    def __init__(self, width, height, fonts, font_sizes, text_colors=None, noise_curve_color="green"):
        self._width = width
        self._height = height
        self._fonts = fonts
        self._font_sizes = font_sizes
        self._text_colors = [Color[x] for x in text_colors] if text_colors is not None else [Color["black"]]
        self._noise_curve_color = Color[noise_curve_color]
        self._truefonts = []
        self._font_sizes_len = len(self._font_sizes)


    @property
    def truefonts(self):
        if self._truefonts:
            return self._truefonts
        self._truefonts = tuple([
            truetype(n, s)
            for n in self._fonts
            for s in self._font_sizes

        ])
        return self._truefonts

    @staticmethod
    def create_noise_line(image, color):
        w, h = image.size
        num = random.randint(0, 3)
        while num:
            x1 = random.randint(0, w)
            y1 = random.randint(0, h)
            x2 = random.randint(0, w)
            y2 = random.randint(0, h)
            points = [x1, y1, x2, y2]

            Draw(image).line(points, fill=color)
            num -= 1
        return image

    @staticmethod
    def random_sin_fill(image):

        x = np.linspace(-10, 10, 1000)
        y = np.sin(x)
        color = random_color(100, 255)

        # 上曲线
        xy = np.asarray(np.stack((x * 30 + random.randint(0, 90), y * 15 - random.randint(2, 10)), axis=1), dtype=int)
        xy = list(map(tuple, xy))
        Draw(image).polygon(xy, fill=color)

        # 下曲线
        xy = np.asarray(np.stack((x * 30 + random.randint(0, 90), y * 15 + random.randint(37, 45)), axis=1), dtype=int)
        xy = list(map(tuple, xy))
        Draw(image).polygon(xy, fill=color)

        return image

    @staticmethod
    def create_noise_dots(image, number=50):

        draw = Draw(image)
        w, h = image.size
        while number:
            x1 = random.randint(0, w)
            y1 = random.randint(0, h)
            draw.point((x1, y1), fill=random_color(0, 255))
            number -= 1
        return image

    def font_choice(self, c: str):

        if c in 'abcdefghijklmnopqrstuvwxyz' or c.isdigit():
            return random.choice(self.truefonts[0:self._font_sizes_len])
        else:
            return random.choice(self.truefonts[self._font_sizes_len:])

    def create_captcha_image(self, chars, background):
        """Create the CAPTCHA image itself.
        :param chars: text to be generated.
        :param background: color of the background.
        """
        image = Image.new('RGB', (self._width, self._height), background)
        image = self.random_sin_fill(image)
        draw = Draw(image)

        def _draw_character(c, color=(255, 255, 255)):
            font = self.font_choice(c)
            w, h = draw.textsize(c, font=font)

            im = Image.new('RGBA', (w, h), color=background)
            Draw(im).text((0, 0), c, font=font, fill=color)

            # rotate
            im = im.crop(im.getbbox())
            im = im.rotate(random.uniform(-30, 30), expand=1)

            fff = Image.new("RGBA", size=im.size, color=background)
            im = Image.composite(im, fff, im)

            return im

        images = []
        colors = ""
        for c in chars:  # 单个字符图片生成
            index = random.randint(0, len(self._text_colors)-1)
            colors += str(index)
            color = self._text_colors[index]
            images.append(_draw_character(c, color))

        start = random.randint(0, 4)
        last_w, _ = images[-1].size # 最后一个字符的宽度
        max_interval = (self._width - last_w - start)//(len(images)-1)  # 字符最大间距，保证不会超出
        # print(max_interval)
        offset = start

        # 字符图片拼接到大图上
        for im in images:
            w, h = im.size
            self.combine(image, im, (offset,  (self._height - h)//2 + random.randint(-2, 2)), background)
            offset = offset + min(max_interval, max(int(0.7*w), 11)) + random.randint(-2, 0)

        return image, colors

    def generate_image(self, chars):
        """Generate the image of the given characters.

        :param chars: text to be generated.
        """
        background = random_color(100, 255, 255)
        im, colors = self.create_captcha_image(chars, background)
        self.create_noise_dots(im)
        self.create_noise_line(im, self._noise_curve_color)
        # im = im.filter(ImageFilter.SMOOTH)
        return im, colors

    @staticmethod
    def combine(image: Image.Image, box, pos, background):

        b_w, b_h = box.size
        start_x, start_y = pos

        image_p = image.load()
        box_p = box.load()

        for i in range(b_w):
            for j in range(b_h):
                b_pixel = box_p[i, j]
                if b_pixel[0:3] == background[0:3]:
                    continue
                else:
                    image_p[start_x + i, start_y + j] = b_pixel[0:3]


def random_color(start, end, opacity=None):
    red = random.randint(start, end)
    green = random.randint(start, end)
    blue = random.randint(start, end)
    if opacity is None:
        return red, green, blue
    return red, green, blue, opacity