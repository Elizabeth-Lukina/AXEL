import spacy
import dateparser

nlp = spacy.load("ru_core_news_md")

INTENT_KEYWORDS = {
    "add_task": ["добавь", "создай", "напомни"],
    "delete_task": ["удали", "убери", "отмени"],
    "reschedule_task": ["перенеси"],
    "list_tasks": ["покажи", "какие задачи", "что у меня"],
    "mark_done": ["выполнил", "готово", "сделано", "выполнено"]
}


def parse_intent(text: str) -> dict:
    doc = nlp(text.lower())
    intent = "unknown"
    task_text = ""
    dt = dateparser.parse(text, settings={"PREFER_DATES_FROM": "future"})

    for token in doc:
        for key, keywords in INTENT_KEYWORDS.items():
            if token.lemma_ in keywords:
                intent = key
                break
        if intent != "unknown":
            break

    if intent in ("add_task", "delete_task", "reschedule_task"):
        for i, token in enumerate(doc):
            if token.lemma_ in INTENT_KEYWORDS[intent]:
                task_text = doc[i + 1:].text.strip()
                break
        task_text = task_text.replace("задачу", "").strip()

    if intent == "add_task":
        return {"intent": "add_task", "task": task_text, "date": dt}
    elif intent == "delete_task":
        return {"intent": "delete_task", "task": task_text, "date": dt}
    elif intent == "reschedule_task":
        return {"intent": "reschedule_task", "task": task_text, "date": dt}
    elif intent == "list_tasks":
        return {"intent": "list_tasks", "date": dt}

    return {"intent": "unknown"}
