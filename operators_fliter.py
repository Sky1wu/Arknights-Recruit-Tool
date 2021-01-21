from data.operators import operators_list
from data.top_operators import top_operators_list
from itertools import combinations


def operators_filter(tags):
    six_star_limited = {}
    five_star_limited = {}
    four_star_limited = {}
    one_star_limited = {}
    normal = {}

    if '高级资深干员' in tags:
        tags.remove('高级资深干员')

        for tag_num in range(2, -1, -1):
            for selected_tag in combinations(tags, tag_num):
                operators = []

                for operator in top_operators_list:
                    if(set(selected_tag).issubset(top_operators_list[operator]['tags'])):
                        operators.append(operator)

                if operators:
                    six_star_limited[('高级资深干员',)+selected_tag] = operators

    for tag_num in range(3, 0, -1):
        for selected_tag in combinations(tags, tag_num):
            operators = []

            for operator in operators_list:
                if(set(selected_tag).issubset(operators_list[operator]['tags'])):
                    operators.append(operator)

            if operators:
                operators.sort(
                    key=lambda operator: operators_list[operator]['level'], reverse=True)

                levels = [operators_list[operator]['level']
                          for operator in operators]

                if 2 in levels or 3 in levels:
                    normal[selected_tag] = operators
                else:
                    min_level = operators_list[operators[-1]]['level']

                    if min_level == 1:
                        one_star_limited[selected_tag] = operators
                    elif min_level == 4:
                        four_star_limited[selected_tag] = operators
                    else:
                        five_star_limited[selected_tag] = operators

    result = {}
    result['6'] = six_star_limited
    result['5'] = five_star_limited
    result['4'] = four_star_limited
    result['1'] = one_star_limited
    result['normal'] = normal

    return result


if __name__ == "__main__":
    tags = ['近战位', '远程位', '治疗', '新手', '群攻']

    result = operators_filter(tags)

    print(result)
