import json

from ark_recruit_tool.config import AppConfig
from ark_recruit_tool.infra.repository import RecruitmentRepository


def test_repository_loads_operator_data():
    repository = RecruitmentRepository(AppConfig())

    operators = repository.list_operators()
    top_operators = repository.list_top_operators()

    assert operators
    assert top_operators
    assert any(operator.name == "Lancet-2" for operator in operators)
    assert any(operator.name == "能天使" for operator in top_operators)


def test_repository_validates_json_schema(tmp_path):
    bad_path = tmp_path / "recruitment.json"
    bad_path.write_text(
        json.dumps(
            {
                "source": "test",
                "generated_at": "not-a-date",
                "operator_count": 1,
                "operators": [{"name": "Lancet-2", "level": 1, "tags": ["支援机械"]}],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    repository = RecruitmentRepository(AppConfig(recruit_data_path=bad_path))

    try:
        repository.list_operators()
    except ValueError as exc:
        assert "generated_at" in str(exc)
    else:
        raise AssertionError("Expected repository schema validation to fail.")
