from flask import Flask, request
from base64 import b64decode
import cv2
from get_tags import get_tags
from operators_fliter import operators_filter
from json2text import json2text
import numpy as np

app = Flask(__name__)


@app.route('/', methods=['POST'])
def recruit():
    status = 0
    if not request.json or 'image' not in request.json:
        msg = '未收到图片！'
    else:
        img_b64 = request.json['image']
        img_b64decode = b64decode(img_b64)
        nparr = np.fromstring(img_b64decode, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        tags = get_tags(img)
        print(tags)

        if len(tags) == 5:
            status = 1
            result = ''

            for tag in tags:
                result += (tag+' ')
            result += '\n\n'

            result_json = operators_filter(tags)
            msg = result + json2text(result_json)
        else:
            msg = 'tag 识别失败'

    response = {
        'status': status,
        'msg': msg
    }

    return response


if __name__ == "__main__":
    app.run()
