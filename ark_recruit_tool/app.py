from __future__ import annotations

import logging
from pathlib import Path

from flask import Flask

from ark_recruit_tool.config import AppConfig
from ark_recruit_tool.domain.analyzer import RecruitmentAnalyzer
from ark_recruit_tool.domain.renderers import LegacyMessageRenderer
from ark_recruit_tool.domain.tags import TagNormalizer
from ark_recruit_tool.infra.donate import DonationRepository
from ark_recruit_tool.infra.image import ImageDecoder, TagImageExtractor, TagImagePreprocessor
from ark_recruit_tool.infra.ocr import TesseractOcrClient
from ark_recruit_tool.infra.repository import RecruitmentRepository
from ark_recruit_tool.services.recruitment import TagRecognitionService
from ark_recruit_tool.web.routes import bp as main_blueprint


def create_app(config_overrides: dict | None = None) -> Flask:
    config = AppConfig.from_mapping(config_overrides)
    app = Flask(
        __name__,
        template_folder=str(Path(__file__).resolve().parent.parent / "templates"),
        static_folder=str(Path(__file__).resolve().parent.parent / "static"),
    )

    _configure_logging(app)
    _register_dependencies(app, config)
    app.register_blueprint(main_blueprint)
    return app


def _configure_logging(app: Flask) -> None:
    if not app.logger.handlers:
        logging.basicConfig(level=logging.INFO)


def _register_dependencies(app: Flask, config: AppConfig) -> None:
    repository = RecruitmentRepository(config)
    analyzer = RecruitmentAnalyzer(repository)
    renderer = LegacyMessageRenderer()
    service = TagRecognitionService(
        image_decoder=ImageDecoder(),
        tag_extractor=TagImageExtractor(),
        preprocessor=TagImagePreprocessor(),
        ocr_client=TesseractOcrClient(config),
        normalizer=TagNormalizer(),
        analyzer=analyzer,
        renderer=renderer,
    )

    app.config["APP_CONFIG"] = config
    app.config["RECRUITMENT_REPOSITORY"] = repository
    app.config["TAG_RECOGNITION_SERVICE"] = service
    app.config["DONATION_REPOSITORY"] = DonationRepository(config.donate_csv_path)
