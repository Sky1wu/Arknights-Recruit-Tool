from ark_recruit_tool.config import AppConfig
from ark_recruit_tool.domain.models import CombinationResult, RecruitResult
from ark_recruit_tool.domain.renderers import LegacyMessageRenderer
from ark_recruit_tool.infra.repository import RecruitmentRepository


def _build_combination(tags, operator_names, operator_lookup):
    return CombinationResult(
        tags=tuple(tags),
        operators=tuple(
            operator_lookup[name]
            for name in operator_names
        ),
    )


def json2text(result_json):
    renderer = LegacyMessageRenderer()
    repository = RecruitmentRepository(AppConfig())
    operator_lookup = {
        operator.name: operator
        for operator in (*repository.list_operators(), *repository.list_top_operators())
    }
    rare = {
        level: tuple(
            _build_combination(selected_tags, operators, operator_lookup)
            for selected_tags, operators in result_json[level].items()
        )
        for level in ("6", "5", "4", "1")
    }
    normal = tuple(
        _build_combination(selected_tags, operators, operator_lookup)
        for selected_tags, operators in result_json["normal"].items()
    )
    return renderer.render(
        RecruitResult(
            status=1,
            rare_combinations=rare,
            normal_combinations=normal,
        )
    )


if __name__ == "__main__":
    tags = ['辅助干员', '近卫干员', '近战位', '特种干员', '群攻']

    result_json = operators_filter(tags)

    result = json2text(result_json)

    print(result)
