from __future__ import annotations

import json
from datetime import datetime, timezone

from ark_recruit_tool.config import AppConfig
from ark_recruit_tool.domain.models import Operator


class RecruitmentRepository:
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._all_operators: tuple[Operator, ...] | None = None

    def list_operators(self) -> tuple[Operator, ...]:
        return tuple(operator for operator in self._load_all() if operator.level < 6)

    def list_top_operators(self) -> tuple[Operator, ...]:
        return tuple(operator for operator in self._load_all() if operator.level >= 6)

    def find_matching_operators(self, selected_tags: tuple[str, ...]) -> tuple[Operator, ...]:
        return self._find_matching(selected_tags, self.list_operators())

    def find_matching_top_operators(self, selected_tags: tuple[str, ...]) -> tuple[Operator, ...]:
        return self._find_matching(selected_tags, self.list_top_operators())

    def _find_matching(
        self,
        selected_tags: tuple[str, ...],
        candidates: tuple[Operator, ...],
    ) -> tuple[Operator, ...]:
        selected = set(selected_tags)
        operators = [operator for operator in candidates if selected.issubset(operator.tags)]
        operators.sort(key=lambda operator: (-operator.level, operator.name))
        return tuple(operators)

    def _load_all(self) -> tuple[Operator, ...]:
        if self._all_operators is None:
            self._all_operators = self._load_json()
        return self._all_operators

    def _load_json(self) -> tuple[Operator, ...]:
        raw_data = json.loads(self._config.recruit_data_path.read_text(encoding="utf-8"))
        self._validate_payload(raw_data)
        return tuple(
            Operator(
                name=operator["name"],
                level=operator["level"],
                tags=frozenset(operator["tags"]),
            )
            for operator in raw_data["operators"]
        )

    def _validate_payload(self, payload: object) -> None:
        if not isinstance(payload, dict):
            raise ValueError("Recruitment data must be a JSON object.")

        required_keys = {"source", "generated_at", "operator_count", "operators"}
        missing = required_keys - set(payload)
        if missing:
            raise ValueError(f"Recruitment data missing required keys: {sorted(missing)}")

        generated_at = payload["generated_at"]
        if not isinstance(generated_at, str):
            raise ValueError("Recruitment data generated_at must be a string.")
        try:
            datetime.fromisoformat(generated_at.replace("Z", "+00:00")).astimezone(timezone.utc)
        except ValueError as exc:
            raise ValueError("Recruitment data generated_at must be a valid ISO 8601 timestamp.") from exc

        operators = payload["operators"]
        if not isinstance(operators, list):
            raise ValueError("Recruitment data operators must be a list.")
        if payload["operator_count"] != len(operators):
            raise ValueError("Recruitment data operator_count does not match operators length.")

        for index, operator in enumerate(operators):
            if not isinstance(operator, dict):
                raise ValueError(f"Recruitment operator at index {index} must be an object.")

            operator_missing = {"name", "level", "tags"} - set(operator)
            if operator_missing:
                raise ValueError(
                    f"Recruitment operator at index {index} missing keys: {sorted(operator_missing)}"
                )

            if not isinstance(operator["name"], str) or not operator["name"]:
                raise ValueError(f"Recruitment operator at index {index} has invalid name.")
            if not isinstance(operator["level"], int):
                raise ValueError(f"Recruitment operator at index {index} has invalid level.")
            if not isinstance(operator["tags"], list) or not all(
                isinstance(tag, str) and tag for tag in operator["tags"]
            ):
                raise ValueError(f"Recruitment operator at index {index} has invalid tags.")
