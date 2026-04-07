from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ark_recruit_tool.constants import UPGRADE_PROMPT
from ark_recruit_tool.domain.analyzer import RecruitmentAnalyzer
from ark_recruit_tool.domain.models import RecruitResult
from ark_recruit_tool.domain.renderers import LegacyMessageRenderer
from ark_recruit_tool.domain.tags import TagNormalizer

if TYPE_CHECKING:
    from ark_recruit_tool.infra.image import ImageDecoder, TagImageExtractor, TagImagePreprocessor
    from ark_recruit_tool.infra.ocr import TesseractOcrClient


logger = logging.getLogger(__name__)


class TagRecognitionService:
    def __init__(
        self,
        image_decoder: ImageDecoder,
        tag_extractor: TagImageExtractor,
        preprocessor: TagImagePreprocessor,
        ocr_client: TesseractOcrClient,
        normalizer: TagNormalizer,
        analyzer: RecruitmentAnalyzer,
        renderer: LegacyMessageRenderer,
    ) -> None:
        self._image_decoder = image_decoder
        self._tag_extractor = tag_extractor
        self._preprocessor = preprocessor
        self._ocr_client = ocr_client
        self._normalizer = normalizer
        self._analyzer = analyzer
        self._renderer = renderer

    def recruit_from_payload(
        self,
        image_base64: str | None,
        client_version: str | None = None,
        current_version: str | None = None,
    ) -> RecruitResult:
        if not image_base64:
            result = RecruitResult(status=0, message="未收到图片！")
            return self._finalize_result(result, client_version, current_version)

        image = self._image_decoder.decode_image(image_base64)
        if image is None:
            result = RecruitResult(status=0, message="图片解析失败")
            return self._finalize_result(result, client_version, current_version)

        tag_images = self._tag_extractor.extract_tag_regions(image)
        recognized_tags: list[str] = []
        for tag_image in tag_images:
            processed = self._preprocessor.preprocess_tag_image(tag_image)
            raw_text = self._ocr_client.recognize_tag(processed)
            normalized = self._normalizer.normalize_tag(raw_text)
            if not normalized:
                logger.warning("OCR returned empty text for a tag region.")
                continue
            recognized_tags.append(normalized)

        if len(recognized_tags) != 5:
            logger.warning("Tag recognition failed: expected 5 tags, got %s.", len(recognized_tags))
            result = RecruitResult(
                status=0,
                recognized_tags=tuple(recognized_tags),
                message="tag 识别失败",
            )
            return self._finalize_result(result, client_version, current_version)

        analysis = self._analyzer.analyze_tags(recognized_tags)
        result = RecruitResult(
            status=1,
            recognized_tags=tuple(recognized_tags),
            rare_combinations=analysis.rare_combinations,
            normal_combinations=analysis.normal_combinations,
        )
        return self._finalize_result(result, client_version, current_version)

    def _finalize_result(
        self,
        result: RecruitResult,
        client_version: str | None,
        current_version: str | None,
    ) -> RecruitResult:
        version_mismatch = bool(current_version and client_version != current_version)
        message = result.message
        if result.status == 1:
            message = self._renderer.render(result, version_mismatch=version_mismatch)
        elif version_mismatch:
            message = f"{UPGRADE_PROMPT}\n\n{result.message}"

        return RecruitResult(
            status=result.status,
            recognized_tags=result.recognized_tags,
            rare_combinations=result.rare_combinations,
            normal_combinations=result.normal_combinations,
            message=message,
        )
