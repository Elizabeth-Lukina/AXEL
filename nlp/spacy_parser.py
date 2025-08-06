import spacy

nlp = spacy.load("ru_core_news_md")

# Простая словарная классификация интентов
INTENT_KEYWORDS = {
    "buy": ["купи", "купить", "покупка", "закажи"],
    "call": ["позвони", "звони", "позвать"],
    "write": ["напиши", "сообщи", "отправь"],
    "remind": ["напомни", "напоминание"]
}

def parse_intent(text: str) -> tuple[str, dict]:
    doc = nlp(text.lower())
    intent = "unknown"
    entities = {}

    # Определим интент по ключевым словам
    for tok in doc:
        for key, keywords in INTENT_KEYWORDS.items():
            if tok.lemma_ in keywords:
                intent = key
                break
        if intent != "unknown":
            break

    # Извлечём объекты (сущности после глагола)
    if intent != "unknown":
        for i, tok in enumerate(doc):
            if tok.lemma_ in INTENT_KEYWORDS[intent]:
                # всё, что справа от глагола — это, скорее всего, объект
                entities["object"] = doc[i+1:].text.strip()
                break

    return intent, entities
