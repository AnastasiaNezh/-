import requests

API_KEY = "29219ddf1d517a3fef4604c6d329e421"


def get_weather(city):
    url = "http://api.weatherstack.com/current"

    params = {
        "access_key": API_KEY,
        "query": city,
        "units": "m"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return f"Ошибка соединения с погодным сервисом для города {city}."

    data = response.json()

    if "error" in data:
        error_info = data["error"].get("info", "Неизвестная ошибка")
        return f"Ошибка API: {error_info}"

    if "current" not in data:
        return f"Не удалось получить данные о погоде для города {city}."

    try:
        current = data["current"]
        temperature = current["temperature"]
        weather_descriptions = current["weather_descriptions"]
        description = weather_descriptions[0] if weather_descriptions else "нет данных"
        wind_speed = current["wind_speed"]

        location_name = data.get("location", {}).get("name", city)

        return (f"Погода в городе {location_name}:\n"
                f"Температура: {temperature}°C\n"
                f"Описание: {description}\n"
                f"Скорость ветра: {wind_speed} м/с")
    except (KeyError, IndexError, TypeError) as e:
        print(f"Ошибка обработки данных: {e}")
        return f"Ошибка при обработке данных о погоде для города {city}."