import spacy
from weather_api import get_weather
from state import DialogState

nlp = spacy.load("ru_core_news_md")

def handle_weather(self, message_text, user_data):
    doc = nlp(message_text)
    city = None

    if user_data["state"] == DialogState.WAIT_CITY:
        for token in doc:
            if token.pos_ in ["PROPN", "NOUN"]:
                city = token.lemma_
                break
        if not city:
            return "Вы написали не город или такого города у меня нет в списках"
    else:
        city = None
        for ent in doc.ents:
            if ent.label_ in ["LOC", "GPE"]:
                city = ent.lemma_
                break

    if city:
        city_cleaned = city.lower().replace("в ", "").strip(",. ")
        if not city_cleaned or city_cleaned == "в":
            user_data["state"] = DialogState.WAIT_CITY
            return "В каком городе вас интересует погода?"

        user_data["state"] = DialogState.START
        return get_weather(city_cleaned.capitalize())

    user_data["state"] = DialogState.WAIT_CITY
    return "В каком городе вас интересует погода?"