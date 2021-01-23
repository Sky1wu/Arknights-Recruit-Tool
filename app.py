from flask import Flask, request, render_template
from base64 import b64decode
import cv2
from get_tags import get_tags
from operators_fliter import operators_filter
from json2text import json2text
import numpy as np
import time
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

version = '1.2'
shortcuts = 'https://www.icloud.com/shortcuts/0aa6e6bb33ff49eeaa0288c4298aa9e2'


def get_time():
    return str(int(time.time()*10**6))


@app.route('/', methods=['GET', 'POST'])
def recruit():
    if request.method == 'POST':
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

        if 'version' not in request.json or request.json['version'] != version:
            msg = '快捷指令有更新，请前往 akhr.imwtx.com 获取最新快捷指令！\n\n'+msg

        response = {
            'status': status,
            'msg': msg
        }

        return response
    else:
        return render_template('index.html', shortcuts=shortcuts, version=version)


if __name__ == "__main__":
    app.run()
