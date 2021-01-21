from operators_fliter import operators_filter
from data.operators import operators_list


def json2text(result_json):
    text = ''

    level_limited = []

    for level in result_json:
        if level == 'normal':
            continue
        if result_json[level]:
            level_limited.append(level)
    if level_limited:
        text += '！！存在稀有 tag 组合！！\n'

        if '1' in level_limited:
            text += ('仅包含 1 星小车或 4 星以上干员\n')
        else:
            next_level = level_limited[-1]
            text += ('仅包含'+next_level+' 星以上干员\n')

        text += '\n'

        for level in result_json:
            if level == 'normal':
                continue
            for selected_tags in result_json[level]:
                text += '-----'
                for tag in selected_tags:
                    text += (tag+' ')
                text += '\b-----\n'

                if '高级资深干员' in selected_tags:
                    text += '★★★★★★: '
                    for operator in result_json[level][selected_tags]:
                        text += (operator+' ')

                else:
                    operator = result_json[level][selected_tags][0]
                    flag = operators_list[operator]['level']
                    now_level = flag
                    for _ in range(flag):
                        text += '★'
                    text += ': '
                    for operator in result_json[level][selected_tags]:
                        now_level = operators_list[operator]['level']
                        if now_level != flag:
                            text += '\n'
                            flag = operators_list[operator]['level']
                            for _ in range(flag):
                                text += '★'
                            text += ': '
                        text += (operator+' ')

                text += '\n'
                text += '\n'

    else:
        text += '未发现稀有 tag 组合\n\n'
        for selected_tags in result_json['normal']:
            text += '----- '
            for tag in selected_tags:
                text += (tag+' ')
            text += '-----\n'

            operator = result_json[level][selected_tags][0]
            flag = operators_list[operator]['level']
            now_level = flag
            for _ in range(flag):
                text += '★'
            text += ': '

            for operator in result_json[level][selected_tags]:
                now_level = operators_list[operator]['level']
                if now_level != flag:
                    text += '\n'
                    flag = operators_list[operator]['level']
                    for _ in range(flag):
                        text += '★'
                    text += ': '
                text += (operator+' ')
            text += '\n'
            text += '\n'

    return text


if __name__ == "__main__":
    tags = ['近卫干员', '重装干员', '特种干员', '治疗', '群攻']

    result_json = operators_filter(tags)

    result = json2text(result_json)

    print(result)
