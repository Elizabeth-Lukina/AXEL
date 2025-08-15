import pytest
from services.nlp.parser import parse_intent
from datetime import datetime, timedelta

@pytest.mark.parametrize("phrase,days_delta", [
    ("завтра", 1),
    ("послезавтра", 2),
])
def test_relative_dates(phrase, days_delta):
    text = f"добавь задачу сделать тз послезавтра {phrase} в 8:00"
    result = parse_intent(text)
    expected_date = (datetime.now() + timedelta(days=days_delta)).date()
    print(f"DEBUG_test {expected_date}")
    assert result["date"].date() == expected_date
    assert result["date"].hour == 8
