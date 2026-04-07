from ark_recruit_tool.config import AppConfig
from ark_recruit_tool.infra.ocr import TesseractOcrClient


_ocr_client = TesseractOcrClient(AppConfig())


def ocr(img):
    return _ocr_client.recognize_tag(img)
