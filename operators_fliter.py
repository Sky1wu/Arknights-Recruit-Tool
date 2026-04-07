from ark_recruit_tool.config import AppConfig
from ark_recruit_tool.domain.analyzer import RecruitmentAnalyzer
from ark_recruit_tool.infra.repository import RecruitmentRepository


def operators_filter(tags):
    repository = RecruitmentRepository(AppConfig())
    analyzer = RecruitmentAnalyzer(repository)
    result = analyzer.analyze_tags(list(tags))

    def to_mapping(combinations):
        return {
            combination.tags: [operator.name for operator in combination.operators]
            for combination in combinations
        }

    return {
        "6": to_mapping(result.rare_combinations["6"]),
        "5": to_mapping(result.rare_combinations["5"]),
        "4": to_mapping(result.rare_combinations["4"]),
        "1": to_mapping(result.rare_combinations["1"]),
        "normal": to_mapping(result.normal_combinations),
    }


if __name__ == "__main__":
    tags = ['近战位', '远程位', '治疗', '新手', '群攻']

    result = operators_filter(tags)

    print(result)
