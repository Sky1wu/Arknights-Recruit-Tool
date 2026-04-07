from ark_recruit_tool.domain.models import RecruitResult

from tests.conftest import build_app


def test_post_root_requires_image():
    app, stub = build_app()
    stub.result = RecruitResult(status=0, message="未收到图片！")

    client = app.test_client()
    response = client.post("/", json={})

    assert response.status_code == 200
    assert response.get_json() == {"status": 0, "msg": "未收到图片！"}
    assert stub.calls[0]["image_base64"] is None


def test_post_root_success_response_shape():
    app, stub = build_app()
    stub.result = RecruitResult(status=1, message="ok")

    client = app.test_client()
    response = client.post("/", json={"image": "encoded", "version": "1.3"})

    assert response.status_code == 200
    assert response.get_json() == {"status": 1, "msg": "ok"}
    assert stub.calls[0]["image_base64"] == "encoded"


def test_post_root_passes_version_for_upgrade_handling():
    app, stub = build_app()
    stub.result = RecruitResult(
        status=0,
        message="快捷指令有更新，请前往 https://akhr.imwtx.com 获取最新快捷指令！\n\ntag 识别失败",
    )

    client = app.test_client()
    response = client.post("/", json={"image": "encoded", "version": "0.9"})

    assert response.status_code == 200
    assert response.get_json()["msg"].startswith("快捷指令有更新")
    assert stub.calls[0]["client_version"] == "0.9"


def test_post_root_returns_json_on_unexpected_error():
    app, stub = build_app()

    def boom(*args, **kwargs):
        raise RuntimeError("boom")

    stub.recruit_from_payload = boom
    client = app.test_client()
    response = client.post("/", json={"image": "encoded", "version": "1.3"})

    assert response.status_code == 500
    assert response.is_json
    assert response.get_json() == {"status": 0, "msg": "服务异常，请稍后重试"}
