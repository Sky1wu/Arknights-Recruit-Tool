from __future__ import annotations

import logging

from flask import Blueprint, current_app, jsonify, render_template, request


bp = Blueprint("main", __name__)
logger = logging.getLogger(__name__)


@bp.get("/")
def index():
    config = current_app.config["APP_CONFIG"]
    return render_template("index.html", shortcuts=config.shortcuts_url, version=config.version)


@bp.post("/")
def recruit():
    payload = request.get_json(silent=True) or {}
    config = current_app.config["APP_CONFIG"]
    service = current_app.config["TAG_RECOGNITION_SERVICE"]
    try:
        result = service.recruit_from_payload(
            image_base64=payload.get("image"),
            client_version=payload.get("version"),
            current_version=config.version,
        )
        return jsonify({"status": result.status, "msg": result.message})
    except Exception:
        logger.exception("Recruitment request failed unexpectedly.")
        return jsonify({"status": 0, "msg": "服务异常，请稍后重试"}), 500


@bp.get("/donate")
def donate():
    records = current_app.config["DONATION_REPOSITORY"].list_records()
    return render_template("donate.html", records=records)
