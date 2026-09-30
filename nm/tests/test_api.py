from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_question_demo_response() -> None:
    response = client.post("/api/qa", json={"text": "Which is the largest ocean?"})
    assert response.status_code == 200
    assert "Pacific" in response.json()["content"]


def test_quiz_has_three_questions_and_four_options() -> None:
    response = client.post("/api/quiz", json={"text": "Pythagorean theorem"})
    assert response.status_code == 200
    questions = response.json()["questions"]
    assert len(questions) == 3
    assert all(len(question["options"]) == 4 for question in questions)
    assert all(question["answer"] in question["options"] for question in questions)


def test_empty_input_is_rejected() -> None:
    response = client.post("/api/explain", json={"topic": ""})
    assert response.status_code == 422
