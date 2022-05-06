import os
import random
import multiprocessing

from PIL import Image

from ImageCaptcha import ImageCaptcha
from color_convert import *

with open("data/chars.txt", "r", encoding="utf-8") as f:
    captcha_cn = f.read()  # 中文字符集

captcha_en = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # 英文字符集

color_dict = ["black", "yellow", "blue", "red"]


def random_str(str_len):
    str = ''
    chars = 'abcdef0123456789'
    length = len(chars) - 1
    for i in range(str_len):
        str += chars[random.randint(0, length)]
    return str


def random_captcha_text(num):

    # 选择2个英文字母（英文字母种类较少，不需要太多，可根据需求自行设置）
    en_num = 4
    cn_num = num - en_num

    example_en = random.sample(captcha_en, en_num)
    example_cn = random.sample(captcha_cn, cn_num)
    example = example_cn + example_en
    random.shuffle(example)

    # 将列表里的片段变为字符串并返回
    verification_code = ''.join(example)
    return verification_code


# 生成字符对应的验证码
def generate_captcha_image(path="fake_pic"):

    imc = ImageCaptcha(width=90, height=35, fonts=[r"data/actionj.ttf", r"data/simsun.ttc"], font_sizes=(24, 25, 26, 27),
                       text_colors=color_dict)

    # 获得随机生成的6个验证码字符
    captcha_text = random_captcha_text(6)

    if not os.path.exists(path):
        print("目录不存在!,已自动创建")
        os.makedirs(path)
    image, colors = imc.generate_image(captcha_text)
    chars_color = {}
    for index, c in enumerate(colors):
        color = color_dict[int(c)]
        old = chars_color.get(color)
        if old is None:
            chars_color.setdefault(color, captcha_text[index])
        else:
            chars_color.update({color: old + captcha_text[index]})

    for key in chars_color.keys():
        copy = image.copy()
        file_name = chars_color.get(key)
        if key == 'black':
            copy = black2red(image)
        elif key == 'blue':
            copy = blue2red(image)
        elif key == 'yellow':
            copy = yellow2red(image)

        file_name += '_' + random_str(32)
        print("生成的验证码的图片为：", file_name)
        copy.save(os.path.join(path, file_name + '.png'))


def gen_single_process():
    # 每个进程生产 1 万个
    for i in range(10000):
        generate_captcha_image()


if __name__ == '__main__':
    # 使用多进程生成
    # gen_single_process()
    process = []
    for i in range(10):
        process.append(
            multiprocessing.Process(target=gen_single_process, args=())
        )
    for p in process:
        p.start()
    for p in process:
        p.join()
    print("generator completed!!!")


