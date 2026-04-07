from ark_recruit_tool.config import AppConfig
from ark_recruit_tool.domain.analyzer import RecruitmentAnalyzer
from ark_recruit_tool.infra.repository import RecruitmentRepository


def test_analyzer_keeps_input_tags_immutable():
    analyzer = RecruitmentAnalyzer(RecruitmentRepository(AppConfig()))
    tags = ["高级资深干员", "输出", "近卫干员", "近战位", "生存"]
    snapshot = list(tags)

    analyzer.analyze_tags(tags)

    assert tags == snapshot


def test_analyzer_builds_top_operator_rare_combinations():
    analyzer = RecruitmentAnalyzer(RecruitmentRepository(AppConfig()))

    result = analyzer.analyze_tags(["高级资深干员", "输出", "近卫干员", "近战位", "生存"])

    top_combinations = result.rare_combinations["6"]
    assert top_combinations
    assert top_combinations[0].tags[0] == "高级资深干员"


def test_analyzer_separates_normal_combinations_with_low_rarity():
    analyzer = RecruitmentAnalyzer(RecruitmentRepository(AppConfig()))

    result = analyzer.analyze_tags(["新手", "术师干员", "远程位", "输出", "群攻"])

    assert result.normal_combinations
    assert any("新手" in combination.tags for combination in result.normal_combinations)
