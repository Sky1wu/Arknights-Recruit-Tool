from ark_recruit_tool.infra.image import TagImagePreprocessor


_preprocessor = TagImagePreprocessor()


def img_preprocess(img):
    return _preprocessor.preprocess_tag_image(img)
