#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen


DEFAULT_SOURCE_URL = (
    "https://raw.githubusercontent.com/"
    "MaaAssistantArknights/MaaAssistantArknights/dev-v2/resource/recruitment.json"
)


def fetch_recruitment(source_url: str) -> dict:
    with urlopen(source_url) as response:
        return json.load(response)


def transform_recruitment(recruitment: dict, source_url: str) -> dict:
    operators = [
        {
            "name": operator["name"],
            "level": operator["rarity"],
            "tags": sorted(operator["tags"]),
        }
        for operator in recruitment["operators"]
    ]
    operators.sort(key=lambda item: (item["level"], item["name"]))
    return {
        "source": source_url,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "operator_count": len(operators),
        "operators": operators,
    }


def load_existing_output(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def has_meaningful_changes(new_payload: dict, existing_payload: dict | None) -> bool:
    if existing_payload is None:
        return True

    keys = ("source", "operator_count", "operators")
    return any(new_payload[key] != existing_payload.get(key) for key in keys)


def merge_generated_at(new_payload: dict, existing_payload: dict | None) -> dict:
    if has_meaningful_changes(new_payload, existing_payload):
        return new_payload

    merged = dict(new_payload)
    merged["generated_at"] = existing_payload["generated_at"]
    return merged


def write_output(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Update Arknights recruit operator data from MaaAssistantArknights."
    )
    parser.add_argument(
        "--source-url",
        default=DEFAULT_SOURCE_URL,
        help="Remote recruitment.json URL",
    )
    parser.add_argument(
        "--output",
        default=str(Path(__file__).resolve().parents[1] / "data" / "recruitment.json"),
        help="Output JSON file path",
    )
    args = parser.parse_args()

    recruitment = fetch_recruitment(args.source_url)
    output_path = Path(args.output)
    existing_payload = load_existing_output(output_path)
    transformed = merge_generated_at(
        transform_recruitment(recruitment, args.source_url),
        existing_payload,
    )
    write_output(output_path, json.dumps(transformed, ensure_ascii=False, indent=2) + "\n")

    print(
        "Updated recruit data:",
        f"{transformed['operator_count']} operators,",
        f"written to {output_path}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
