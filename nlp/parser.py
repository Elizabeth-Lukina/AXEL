import re
import dateparser

def parse_intent(text):
    text = text.lower().strip()

    # Удалить задачу
    match = re.search(r"удали(ть)? задачу (.+)", text)
    if match:
        return {"intent": "delete", "task": match.group(2)}

    # Перенести задачу
    match = re.search(r"перенеси(ть)? задачу(?: (.+?))? на (.+)", text)
    if match:
        return {
            "intent": "reschedule",
            "task": match.group(2),
            "date": dateparser.parse(match.group(3))
        }

    # Добавить задачу
    match = re.search(r"(добавь|напомни|создай) (?:мне )?задачу (.+)", text)
    if match:
        parsed_date = dateparser.parse(text)
        return {
            "intent": "add",
            "task": match.group(2),
            "date": parsed_date
        }

    # Показать задачи
    match = re.search(r"(что у меня|какие задачи|покажи задачи)(.*)", text)
    if match:
        parsed_date = dateparser.parse(text)
        return {
            "intent": "list",
            "date": parsed_date
        }

    return {"intent": "unknown"}
