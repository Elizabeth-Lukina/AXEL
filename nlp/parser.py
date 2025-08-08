import spacy
import dateparser

nlp = spacy.load("ru_core_news_md")

INTENT_KEYWORDS = {
    "add_task": ["добавь", "создай", "напомни"],
    "delete_task": ["удали", "убери", "отмени"],
    "reschedule_task": ["перенеси"],
    "complete_task": ["выполнил", "сделал", "готово", "закрыть", "отметь"],
    "list_tasks": ["покажи", "какие задачи", "что у меня"]
}

def parse_intent(text: str) -> dict:
    doc = nlp(text.lower())
    intent = "unknown"
    task_text = ""
    dt = dateparser.parse(text)

    for token in doc:
        for key, keywords in INTENT_KEYWORDS.items():
            if token.lemma_ in keywords:
                intent = key
                break
        if intent != "unknown":
            break

    if intent in ("add_task", "delete_task", "reschedule_task", "complete_task"):
        for i, token in enumerate(doc):
            if token.lemma_ in INTENT_KEYWORDS[intent]:
                task_text = doc[i + 1:].text.strip()
                break
        return {
            "intent": intent,
            "task": task_text,
            "date": dt
        }

    elif intent == "list_tasks":
        return {"intent": "list_tasks", "date": dt}

    return {"intent": "unknown"}