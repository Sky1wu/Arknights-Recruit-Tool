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
    transformed = transform_recruitment(recruitment, args.source_url)
    output_path = Path(args.output)
    write_output(output_path, json.dumps(transformed, ensure_ascii=False, indent=2) + "\n")

    print(
        "Updated recruit data:",
        f"{transformed['operator_count']} operators,",
        f"written to {output_path}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
