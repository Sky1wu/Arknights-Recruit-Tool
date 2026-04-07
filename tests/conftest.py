from __future__ import annotations

from ark_recruit_tool import create_app


class StubService:
    def __init__(self) -> None:
        self.result = None
        self.calls = []

    def recruit_from_payload(self, image_base64, client_version=None, current_version=None):
        self.calls.append(
            {
                "image_base64": image_base64,
                "client_version": client_version,
                "current_version": current_version,
            }
        )
        return self.result


def build_app():
    app = create_app(
        {
            "version": "1.3",
            "shortcuts_url": "https://example.com/shortcut",
        }
    )
    app.config["TESTING"] = True
    stub = StubService()
    app.config["TAG_RECOGNITION_SERVICE"] = stub
    return app, stub
