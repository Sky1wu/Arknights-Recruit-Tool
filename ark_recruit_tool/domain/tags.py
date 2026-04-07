from __future__ import annotations

import difflib

from ark_recruit_tool.constants import VALID_TAGS


class TagNormalizer:
    def __init__(self, valid_tags: tuple[str, ...] = VALID_TAGS) -> None:
        self._valid_tags = valid_tags

    def normalize_tag(self, text: str) -> str:
        cleaned = text.replace(" ", "").strip()
        if not cleaned:
            return ""
        return max(
            self._valid_tags,
            key=lambda tag: difflib.SequenceMatcher(None, tag, cleaned).quick_ratio(),
        )
