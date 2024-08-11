import cv2
import numpy as np
# from PIL import Image


def threshold(img):
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bwimg1 = cv2.threshold(grayimg, 120, 255, cv2.THRESH_BINARY)
    _, bwimg2 = cv2.threshold(grayimg, 120, 255, cv2.THRESH_TOZERO)
    return bwimg1, bwimg2


def find_text_area(img):
    kernel = np.ones((1, 11), np.uint8)
    dilation = cv2.dilate(img, kernel, iterations=1)  # 膨胀

    contours, _ = cv2.findContours(
        dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 寻找轮廓

    text_area = max(contours, key=lambda x: cv2.contourArea(x))  # 确定文字区域

    rect = cv2.minAreaRect(text_area)  # 文字区域的最小外接矩形

    return rect


def fill_outside(img, contour):
    box = cv2.boxPoints(contour)
    box = np.int0(box)

    stencil = np.zeros(img.shape).astype(img.dtype)
    color = [255, 255, 255]
    cv2.fillPoly(stencil, [box], color)

    result = cv2.bitwise_and(img, stencil)

    return result


def img_preprocess(img):
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (320, 100))

    bwimg1, bwimg2 = threshold(img)

    text_area = find_text_area(bwimg1)

    result = fill_outside(bwimg2, text_area)

    # image = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))

    return result
