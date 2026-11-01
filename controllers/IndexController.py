
from flask import Blueprint

index_bp = Blueprint(
    'index', __name__
)


@index_bp.route("/")
def index():
    return {"versao": "1.0.0"}, 200


@index_bp.route("/health")
def health():
    return {"health": "ok"}, 200
