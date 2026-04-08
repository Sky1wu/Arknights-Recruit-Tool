from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "update_recruit_data.py"
SPEC = importlib.util.spec_from_file_location("update_recruit_data", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_merge_generated_at_preserves_timestamp_when_content_is_unchanged():
    existing = {
        "source": "https://example.com/recruitment.json",
        "generated_at": "2026-04-08T00:00:00Z",
        "operator_count": 1,
        "operators": [{"name": "Lancet-2", "level": 1, "tags": ["治疗"]}],
    }
    new_payload = {
        "source": "https://example.com/recruitment.json",
        "generated_at": "2026-04-08T01:00:00Z",
        "operator_count": 1,
        "operators": [{"name": "Lancet-2", "level": 1, "tags": ["治疗"]}],
    }

    merged = MODULE.merge_generated_at(new_payload, existing)

    assert merged["generated_at"] == "2026-04-08T00:00:00Z"


def test_merge_generated_at_updates_timestamp_when_operator_content_changes():
    existing = {
        "source": "https://example.com/recruitment.json",
        "generated_at": "2026-04-08T00:00:00Z",
        "operator_count": 1,
        "operators": [{"name": "Lancet-2", "level": 1, "tags": ["治疗"]}],
    }
    new_payload = {
        "source": "https://example.com/recruitment.json",
        "generated_at": "2026-04-08T01:00:00Z",
        "operator_count": 2,
        "operators": [
            {"name": "Lancet-2", "level": 1, "tags": ["治疗"]},
            {"name": "Castle-3", "level": 1, "tags": ["支援"]},
        ],
    }

    merged = MODULE.merge_generated_at(new_payload, existing)

    assert merged["generated_at"] == "2026-04-08T01:00:00Z"
