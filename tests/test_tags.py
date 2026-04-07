from ark_recruit_tool.domain.tags import TagNormalizer


def test_normalize_tag_picks_closest_valid_tag():
    normalizer = TagNormalizer()

    assert normalizer.normalize_tag("高级资深千员") == "高级资深干员"
    assert normalizer.normalize_tag("快速复话") == "快速复活"
