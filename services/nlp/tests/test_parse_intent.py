from datetime import datetime, timedelta
from services.nlp.parser import parse_intent


def test_add_task_with_tomorrow():
    text = "добавь задачу купить хлеб завтра в 10:30"
    result = parse_intent(text)

    assert result["intent"] == "add_task"
    assert "купить хлеб" in result["task"]
    assert result["date"] is not None

    expected_date = (datetime.now() + timedelta(days=1)).date()
    assert result["date"].date() == expected_date
    assert result["date"].hour == 10
    assert result["date"].minute == 30


def test_delete_task():
    text = "удали задачу купить молоко"
    result = parse_intent(text)
    assert result["intent"] == "delete_task"
    assert "молоко" in result["task"]
