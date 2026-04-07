from __future__ import annotations

from ark_recruit_tool.constants import RARE_LEVEL_ORDER, UPGRADE_PROMPT
from ark_recruit_tool.domain.models import CombinationResult, RecruitResult


class LegacyMessageRenderer:
    def render(self, result: RecruitResult, version_mismatch: bool = False) -> str:
        body = self._build_body(result)
        if version_mismatch:
            if body:
                return f"{UPGRADE_PROMPT}\n\n{body}"
            return UPGRADE_PROMPT
        return body

    def _build_body(self, result: RecruitResult) -> str:
        sections: list[str] = []
        if result.recognized_tags:
            sections.append(" ".join(result.recognized_tags))

        rare_entries = {
            level: combinations
            for level, combinations in result.rare_combinations.items()
            if combinations
        }
        if rare_entries:
            sections.append(self._render_rare_section(rare_entries))
        else:
            sections.append(self._render_normal_section(result.normal_combinations))

        return "\n\n".join(section for section in sections if section)

    def _render_rare_section(
        self,
        rare_entries: dict[str, tuple[CombinationResult, ...]],
    ) -> str:
        lines = ["！！存在稀有 tag 组合！！", ""]
        for level in RARE_LEVEL_ORDER:
            for combination in rare_entries.get(level, ()):
                lines.extend(self._render_combination(combination))
                lines.append("")
        return "\n".join(lines).strip()

    def _render_normal_section(self, combinations: tuple[CombinationResult, ...]) -> str:
        if not combinations:
            return "未发现稀有 tag 组合"

        lines = ["未发现稀有 tag 组合", ""]
        for combination in combinations:
            lines.extend(self._render_combination(combination))
            lines.append("")
        return "\n".join(lines).strip()

    def _render_combination(self, combination: CombinationResult) -> list[str]:
        header = f"----- {' '.join(combination.tags)} -----"
        grouped_lines: list[str] = []
        current_level: int | None = None
        current_names: list[str] = []

        def flush() -> None:
            if current_level is None:
                return
            stars = "★" * current_level
            grouped_lines.append(f"{stars}: {' '.join(current_names)}")

        for operator in combination.operators:
            if operator.level != current_level:
                flush()
                current_level = operator.level
                current_names = [operator.name]
            else:
                current_names.append(operator.name)

        flush()
        return [header, *grouped_lines]
