from __future__ import annotations

import logging
from shlex import quote

import pytesseract

from ark_recruit_tool.config import AppConfig
from ark_recruit_tool.constants import OCR_CHAR_WHITELIST


logger = logging.getLogger(__name__)


class TesseractOcrClient:
    def __init__(self, config: AppConfig) -> None:
        self._config = config

    def recognize_tag(self, image) -> str:
        tessdata_dir = self._resolve_tessdata_dir()
        text = pytesseract.image_to_string(
            image,
            lang=self._config.ocr_lang,
            config=(
                f"--tessdata-dir {quote(str(tessdata_dir))} "
                "--dpi 300 --oem 0 --psm 8 "
                f"-c tessedit_char_whitelist={OCR_CHAR_WHITELIST}"
            ),
        )
        return text.replace(" ", "").replace("\n\x0c", "")

    def _resolve_tessdata_dir(self):
        if self._config.ocr_model_path.exists():
            return self._config.ocr_model_path.parent

        logger.warning(
            "OCR traineddata file not found at %s, falling back to configured tessdata dir %s.",
            self._config.ocr_model_path,
            self._config.ocr_data_dir,
        )
        return self._config.ocr_data_dir
