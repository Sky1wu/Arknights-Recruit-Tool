from ark_recruit_tool.domain.tags import TagNormalizer
from ark_recruit_tool.infra.image import TagImageExtractor, TagImagePreprocessor
from ark_recruit_tool.infra.ocr import TesseractOcrClient
from ark_recruit_tool.config import AppConfig


_extractor = TagImageExtractor()
_preprocessor = TagImagePreprocessor()
_ocr_client = TesseractOcrClient(AppConfig())
_normalizer = TagNormalizer()


def correct_tag(text):
    return _normalizer.normalize_tag(text)


def identify_tags_img(img):
    return _extractor.extract_tag_regions(img)


def get_tags(img):
    tags = []
    for tag in identify_tags_img(img):
        processed = _preprocessor.preprocess_tag_image(tag)
        tags.append(correct_tag(_ocr_client.recognize_tag(processed)))
    return [tag for tag in tags if tag]


if __name__ == "__main__":
    img = cv2.imread('test_img/6.png')
    tags = get_tags(img)
    print(tags)
