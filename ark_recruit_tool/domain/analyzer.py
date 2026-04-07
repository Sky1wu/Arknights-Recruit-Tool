from __future__ import annotations

from itertools import combinations

from ark_recruit_tool.domain.models import CombinationResult, RecruitAnalysis
from ark_recruit_tool.infra.repository import RecruitmentRepository


class RecruitmentAnalyzer:
    def __init__(self, repository: RecruitmentRepository) -> None:
        self._repository = repository

    def analyze_tags(self, tags: list[str] | tuple[str, ...]) -> RecruitAnalysis:
        input_tags = list(tags)
        rare: dict[str, list[CombinationResult]] = {"6": [], "5": [], "4": [], "1": []}
        normal: list[CombinationResult] = []

        top_tag = "高级资深干员"
        non_top_tags = [tag for tag in input_tags if tag != top_tag]
        if top_tag in input_tags:
            for tag_count in range(2, -1, -1):
                for selected_tag in combinations(non_top_tags, tag_count):
                    operators = self._repository.find_matching_top_operators(selected_tag)
                    if operators:
                        rare["6"].append(
                            CombinationResult(tags=(top_tag,) + selected_tag, operators=operators)
                        )

        for tag_count in range(3, 0, -1):
            for selected_tag in combinations(input_tags, tag_count):
                operators = self._repository.find_matching_operators(selected_tag)
                if not operators:
                    continue

                levels = {operator.level for operator in operators}
                result = CombinationResult(tags=selected_tag, operators=operators)
                if 2 in levels or 3 in levels:
                    normal.append(result)
                    continue

                min_level = min(levels)
                if min_level == 1:
                    rare["1"].append(result)
                elif min_level == 4:
                    rare["4"].append(result)
                else:
                    rare["5"].append(result)

        return RecruitAnalysis(
            rare_combinations={key: tuple(value) for key, value in rare.items()},
            normal_combinations=tuple(normal),
        )
