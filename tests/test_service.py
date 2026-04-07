from ark_recruit_tool.config import AppConfig
from ark_recruit_tool.domain.analyzer import RecruitmentAnalyzer
from ark_recruit_tool.domain.renderers import LegacyMessageRenderer
from ark_recruit_tool.domain.tags import TagNormalizer
from ark_recruit_tool.infra.ocr import TesseractOcrClient
from ark_recruit_tool.infra.repository import RecruitmentRepository
from ark_recruit_tool.services.recruitment import TagRecognitionService


class StubDecoder:
    def decode_image(self, image_base64):
        return {"payload": image_base64}


class StubExtractor:
    def __init__(self, count=5):
        self.count = count

    def extract_tag_regions(self, image):
        return [f"tag-{index}" for index in range(self.count)]


class StubPreprocessor:
    def preprocess_tag_image(self, image):
        return image


class StubOcr:
    def __init__(self, texts):
        self.texts = list(texts)

    def recognize_tag(self, image):
        return self.texts.pop(0)


def build_service(ocr_texts, count=5):
    analyzer = RecruitmentAnalyzer(RecruitmentRepository(AppConfig()))
    return TagRecognitionService(
        image_decoder=StubDecoder(),
        tag_extractor=StubExtractor(count=count),
        preprocessor=StubPreprocessor(),
        ocr_client=StubOcr(ocr_texts),
        normalizer=TagNormalizer(),
        analyzer=analyzer,
        renderer=LegacyMessageRenderer(),
    )


def test_service_handles_missing_image():
    service = build_service([])

    result = service.recruit_from_payload(None, current_version="1.3")

    assert result.status == 0
    assert result.message == "快捷指令有更新，请前往 https://akhr.imwtx.com 获取最新快捷指令！\n\n未收到图片！"


def test_service_returns_success_with_five_tags():
    service = build_service(["高级资深干员", "输出", "近卫干员", "近战位", "生存"])

    result = service.recruit_from_payload("encoded", client_version="1.3", current_version="1.3")

    assert result.status == 1
    assert result.recognized_tags == ("高级资深干员", "输出", "近卫干员", "近战位", "生存")
    assert "！！存在稀有 tag 组合！！" in result.message


def test_service_returns_failure_when_tag_count_is_not_five():
    service = build_service(["输出", "近卫干员", "近战位", "生存"], count=4)

    result = service.recruit_from_payload("encoded", client_version="1.3", current_version="1.3")

    assert result.status == 0
    assert result.message == "tag 识别失败"


def test_tesseract_client_uses_project_tessdata_dir(tmp_path, monkeypatch):
    traineddata = tmp_path / "ark_recruit.traineddata"
    traineddata.write_text("stub", encoding="utf-8")
    captured = {}

    def fake_image_to_string(image, lang, config):
        captured["lang"] = lang
        captured["config"] = config
        return "输出"

    monkeypatch.setattr("pytesseract.image_to_string", fake_image_to_string)
    client = TesseractOcrClient(
        AppConfig(
            ocr_model_path=traineddata,
            ocr_data_dir=tmp_path,
        )
    )

    result = client.recognize_tag("image")

    assert result == "输出"
    assert captured["lang"] == "ark_recruit"
    assert f"--tessdata-dir {tmp_path}" in captured["config"]
