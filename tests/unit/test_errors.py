from fastapi import FastAPI
from fastapi.testclient import TestClient

from gamemind.core.errors import AppError, NotReadyError, register_exception_handlers


def test_app_error_handler_returns_json() -> None:
    test_app = FastAPI()
    register_exception_handlers(test_app)

    @test_app.get("/boom")
    def boom() -> None:
        raise AppError("bad request")

    response = TestClient(test_app).get("/boom")
    assert response.status_code == 400
    assert response.json() == {"detail": "bad request"}


def test_not_ready_error_defaults_to_503() -> None:
    test_app = FastAPI()
    register_exception_handlers(test_app)

    @test_app.get("/not-ready")
    def not_ready() -> None:
        raise NotReadyError()

    response = TestClient(test_app).get("/not-ready")
    assert response.status_code == 503
    assert response.json()["detail"] == "Recommendation index is not ready."
