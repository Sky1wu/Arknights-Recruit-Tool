import pytesseract


def ocr(img):
    whitelist = '高级远程位输出狙击干员近战支援卫治疗医防护重装爆发生存群攻削弱术师费用回复先锋特种资深机械移减速新手控场快活辅助召唤元素'

    text = pytesseract.image_to_string(
        img, lang='ark_recruit', config='--dpi 300 --oem 0 --psm 8 -c tessedit_char_whitelist='+whitelist)

    text = text.replace(' ', '').replace('\n\x0c', '')

    return text
