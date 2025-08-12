import re
import spacy
from dateparser.search import search_dates
from dateparser import parse as dp_parse
from typing import Optional
from datetime import datetime

nlp = spacy.load("ru_core_news_md")

INTENT_KEYWORDS = {
    "add_task": ["добавь", "создай", "напомни", "запиши", "добавить"],
    "delete_task": ["удали", "убери", "отмени", "удалить"],
    "reschedule_task": ["перенеси", "перенос", "перенести"],
    "list_tasks": ["покажи", "какие", "список", "что у меня"],
    "complete_task": ["выполнил", "сделал", "готово", "выполнено", "закрыл", "закончено"]
}


def normalize_time_format(text: str) -> str:
    # 10.40 -> 10:40, 9.5 -> 9:05 не трогаем (только XX.XX)
    text = re.sub(r"\b(\d{1,2})\.(\d{2})\b", r"\1:\2", text)
    # убрать лишние слова типа "утра/вечера" после времени (dateparser нормально их трактует)
    return text


def find_date_in_text(text: str) -> Optional[datetime]:
    """
    Попытаться найти дату/время в тексте. Возвращает datetime или None.
    Использует dateparser.search.search_dates если возможно, fallback на dateparser.parse.
    """
    norm = normalize_time_format(text)
    try:
        res = search_dates(norm, languages=["ru"])
    except Exception:
        res = None

    if res:
        # выбираем последнюю найденную дату (часто в конце)
        _, dt = res[-1]
        return dt
    # fallback
    try:
        dt = dp_parse(norm, languages=["ru"])
        return dt
    except Exception:
        return None


def remove_date_substring(text: str, dt_substring: Optional[str]) -> str:
    if not dt_substring:
        return text
    return text.replace(dt_substring, "").strip()


def clean_task_text(text: str, intent: str) -> str:
    """
    Удаляет триггерные слова (например: 'добавь', 'задачу', 'напомни мне') и
    также удаления найденной даты-подстроки делаем в вызывающем коде.
    """
    doc = nlp(text.lower())
    triggers = set()
    for kws in INTENT_KEYWORDS.values():
        triggers.update(kws)
    tokens = [t.text for t in doc if t.lemma_ not in triggers and t.text not in ("задача", "задачу", "мне")]
    cleaned = " ".join(tokens).strip()
    # ещё убрать двоеточия/лишние пробелы
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or None


def parse_intent(text: str) -> dict:
    original = text.strip()
    norm = normalize_time_format(original)
    doc = nlp(norm)
    intent = "unknown"

    # 1. Определяем intent по ключевым словам
    for token in doc:
        for key, kws in INTENT_KEYWORDS.items():
            if token.lemma_ in kws:
                intent = key
                break
        if intent != "unknown":
            break

    # 2. Ищем дату/время
    date_substring = None
    date_obj = None

    try:
        res = search_dates(norm, languages=["ru"])
    except Exception:
        res = None

    if res:
        # Ищем именно дату с временем, иначе берём первую попавшуюся дату
        dt_with_time = [(m, d) for m, d in res if d.hour != 0 or d.minute != 0]
        if dt_with_time:
            match_str, date_obj = dt_with_time[-1]
        else:
            match_str, date_obj = res[-1]
        date_substring = match_str
    else:
        try:
            date_obj = dp_parse(norm, languages=["ru"])
        except Exception:
            date_obj = None

    # 3. Если intent не определён, но есть дата → считаем add_task
    if intent == "unknown" and date_obj:
        intent = "add_task"

    # 4. Удаляем подстроку даты
    text_wo_date = norm
    if date_substring:
        text_wo_date = re.sub(re.escape(date_substring), " ", text_wo_date, flags=re.IGNORECASE)

    # 5. Чистим текст задачи
    task_text = clean_task_text(text_wo_date, intent)

    return {
        "intent": intent,
        "task": task_text,
        "date": date_obj,
        "date_substring": date_substring
    }



# Тест (локально)
if __name__ == "__main__":
    tests = [
        "добавь купить капусту завтра в 10.40 утра",
        "напомни позвонить маме через 2 часа"
    ]
    for t in tests:
        print(t, "->", parse_intent(t))
