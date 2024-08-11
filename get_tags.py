import cv2
from img_preprocess import img_preprocess
from ocr import ocr
import difflib


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


def correct_tag(text):
    '''
    矫正 OCR 的识别结果，取与 tags 中最相似的
    '''

    tags = ['特种干员', '近战位', '输出', '生存', '近卫干员', '支援', '支援机械', '狙击干员', '远程位', '位移', '减速', '术师干员', '新手', '先锋干员',
            '费用回复', '群攻', '医疗干员', '治疗', '控场', '快速复活', '重装干员', '防护', '爆发', '辅助干员', '削弱', '召唤', '高级资深干员', '资深干员', '元素']

    tag = max(tags, key=lambda tag: string_similar(tag, text))

    return tag


def identify_tags_img(img):
    '''
    从截图中截取 5 个 tag 图片
    '''

    height, width = img.shape[0], img.shape[1]
    new_width = int(width/height*1080)

    img = cv2.resize(img, (new_width, 1080))  # 强制缩放图片，高为 1080

    offset = int(new_width/20)  # 因 tag 区域并非图片的正中央，此值裁剪图片的偏移量

    y1 = int(new_width/2*1/2)-offset
    y2 = new_width-y1-offset

    img = img[270:810, y1:y2]

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转为灰度图

    _, bin_img = cv2.threshold(gray_img, 80, 255, cv2.THRESH_BINARY_INV)  # 二值化

    contours, _ = cv2.findContours(
        bin_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 寻找轮廓

    cv_contours = []

    # 筛选轮廓，多边形逼近后为 4 边形且面积 > 7000
    for cnt in contours:
        length = cv2.arcLength(cnt, True)
        area = cv2.contourArea(cnt)
        cnt = cv2.approxPolyDP(cnt, 0.025*length, True)

        if len(cnt) == 4 and cv2.isContourConvex(cnt) and area > 7000:
            cv_contours.append(cnt)

    tags_img = []

    # 上轮筛选过后，cv_contours 应该会包括 5 个 tag 以及招募时限中加减时间的按钮
    # 如果无意外，前 5 个应该就是 5 个 tag 的倒序排列
    # 如果事先不裁剪图片，这里可能会多一个确认招募的按钮影响结果
    for tag in cv_contours[4::-1]:
        x, y, w, h = cv2.boundingRect(tag)
        tag = img[y:y+h, x:x+w]
        tags_img.append(tag)

    return tags_img


def get_tags(img):
    tags_img = identify_tags_img(img)
    tags = []

    for tag in tags_img:
        tag_img = img_preprocess(tag)
        text = ocr(tag_img)
        tag = correct_tag(text)
        tags.append(tag)

    return tags


if __name__ == "__main__":
    img = cv2.imread('test_img/6.png')
    tags = get_tags(img)
    print(tags)
