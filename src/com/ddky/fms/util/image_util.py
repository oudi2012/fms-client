# -*- coding: utf-8 -*-

from PIL import Image


def remove_background(src_image, desPath):
    img = Image.open(src_image)
    img = img.convert("RGBA")  # 转换获取信息
    pixData = img.load()

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixData[x, y][0] > 40 and pixData[x, y][1] > 40 and pixData[x, y][2] > 40 and pixData[x, y][3] > 40:
                pixData[x, y] = (255, 255, 255, 0)
    img.save(desPath)


if __name__ == "__main__":
    src_path = "../images/start.png"
    desPath = "../images/start_no.png"
    remove_background(src_path, desPath)
