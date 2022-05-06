#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2022/4/28 6:24 PM 
# @Author : QiangXu 
# @Version：V 0.1
# @File : color_convert.py

import cv2
import numpy
from PIL import Image


def blue2red(im: Image):
    """
    蓝转红
    :param im: 原始图片
    :return: 转化后的图片
    """
    img = cv2.cvtColor(numpy.asarray(im), cv2.COLOR_RGB2BGR)
    # 蓝色R、G值较小，B值独大，B、G交换，接近红色分布
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def black2red(im: Image):
    """
    黑转红
    :param im: 原始图片
    :return: 转化后的图片
    """
    img = cv2.cvtColor(numpy.asarray(im), cv2.COLOR_RGB2BGR)
    img[:, :, 2] = 255 - img[:, :, 2]  # 黑色三个通道都比较小， 用255-R通道，则R通道独大，其余通道小，接近红色的分布
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def yellow2red(im: Image):
    """
    黄转红
    :param im: 原始图片
    :return: 转化后的图片
    """
    img = cv2.cvtColor(numpy.asarray(im), cv2.COLOR_RGB2BGR)
    img = cv2.bitwise_not(img)  # 黄色R、G值较大，B值较小，先取反，则R、G值较小, B值独大，接近蓝色分布
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # 与蓝色转红色相同
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))