from ark_recruit_tool.domain.models import CombinationResult, Operator, RecruitResult
from ark_recruit_tool.domain.renderers import LegacyMessageRenderer


def make_operator(name: str, level: int) -> Operator:
    return Operator(name=name, level=level, tags=frozenset())


def test_renderer_formats_rare_section():
    renderer = LegacyMessageRenderer()
    result = RecruitResult(
        status=1,
        recognized_tags=("高级资深干员", "输出", "近卫干员", "近战位", "生存"),
        rare_combinations={
            "6": (
                CombinationResult(
                    tags=("高级资深干员", "输出"),
                    operators=(make_operator("史尔特尔", 6),),
                ),
            ),
            "5": (),
            "4": (),
            "1": (),
        },
    )

    text = renderer.render(result)

    assert "！！存在稀有 tag 组合！！" in text
    assert "★★★★★★: 史尔特尔" in text


def test_renderer_formats_normal_section_without_level_leak():
    renderer = LegacyMessageRenderer()
    result = RecruitResult(
        status=1,
        normal_combinations=(
            CombinationResult(
                tags=("输出", "远程位"),
                operators=(
                    make_operator("能天使", 6),
                    make_operator("四月", 5),
                    make_operator("克洛丝", 3),
                ),
            ),
        ),
    )

    text = renderer.render(result)

    assert "未发现稀有 tag 组合" in text
    assert "★★★★★★: 能天使" in text
    assert "★★★★★: 四月" in text
    assert "★★★: 克洛丝" in text
