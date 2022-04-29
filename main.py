import os
import random
from ImageCaptcha import ImageCaptcha

with open("data/chars.txt", "r", encoding="utf-8") as f:
    captcha_cn = f.read()  # 中文字符集

captcha_en = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # 英文字符集

color_dict = ["黑", "黄", "蓝", "红"]


def random_str(str_len):
    str = ''
#    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    chars = 'abcdef0123456789'
    length = len(chars) - 1
    for i in range(str_len):
        str += chars[random.randint(0, length)]
    return str


def random_captcha_text(num):

    # 选择0-2个英文字母（英文字母种类较少，不需要太多，可根据需求自行设置）
    en_num = random.randint(0, 2)
    cn_num = num - en_num

    example_en = random.sample(captcha_en, en_num)
    example_cn = random.sample(captcha_cn, cn_num)
    example = example_cn + example_en
    random.shuffle(example)

    # 将列表里的片段变为字符串并返回
    verification_code = ''.join(example)
    return verification_code


# 生成字符对应的验证码
def generate_captcha_image(path="fake_pic", num=1):

    imc = ImageCaptcha(width=90, height=35, fonts=[r"data/actionj.ttf", r"data/simsun.ttc"], font_sizes=(18, 19),
                       text_colors=["black", "yellow", "blue", "red"])

    # 获得随机生成的6个验证码字符
    captcha_text = random_captcha_text(6)

    if not os.path.exists(path):
        print("目录不存在!,已自动创建")
        os.makedirs(path)
    for _ in range(num):
        image, colors = imc.generate_image(captcha_text)
        # 取出是红色的
        has_red = False
        file_name = ''
        for index, c in enumerate(colors):
            if color_dict[int(c)] == '红':
                has_red = True
                file_name += (captcha_text[index])
        if not has_red:
            continue
        file_name += '_' + random_str(32)
        print("生成的验证码的图片为：", file_name)
        image.save(os.path.join(path, file_name + '.png'))


if __name__ == '__main__':
    for i in range(100000):
        generate_captcha_image(num=3)


