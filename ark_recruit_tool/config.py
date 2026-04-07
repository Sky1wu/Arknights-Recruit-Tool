from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class AppConfig:
    version: str = "1.3"
    shortcuts_url: str = "https://www.icloud.com/shortcuts/ba65fd65334d48bb9d9ba0ae89e17a85"
    recruit_data_path: Path = BASE_DIR / "data" / "recruitment.json"
    donate_csv_path: Path = BASE_DIR / "donate.csv"
    ocr_lang: str = "ark_recruit"
    ocr_model_path: Path = BASE_DIR / "ark_recruit.traineddata"
    ocr_data_dir: Path = BASE_DIR

    @classmethod
    def from_mapping(cls, overrides: dict | None = None) -> "AppConfig":
        if not overrides:
            return cls()

        data = dict(overrides)
        if "recruit_data_path" in data:
            data["recruit_data_path"] = Path(data["recruit_data_path"])
        if "donate_csv_path" in data:
            data["donate_csv_path"] = Path(data["donate_csv_path"])
        if "ocr_model_path" in data:
            data["ocr_model_path"] = Path(data["ocr_model_path"])
        if "ocr_data_dir" in data:
            data["ocr_data_dir"] = Path(data["ocr_data_dir"])
        return cls(**data)
