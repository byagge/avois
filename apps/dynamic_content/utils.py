import random
import requests
from datetime import datetime

# Список сообщений для разного времени суток
TIME_MESSAGES = {
    "night": [
        "А не пора спать? Завтра сможете продолжить.",
        "Поздняя ночь – пора для отдыха!",
        "Ночной покой лучше всего для работы завтра.",
        "Закрывайте глаза и отдыхайте.",
        "Пусть сон принесет вам вдохновение!"
    ],
    "morning": [
        "Доброе утро! Новый день – новые возможности!",
        "Как прошло ваше утро?",
        "Сегодня отличный день для достижений!",
        "Желаем вам продуктивного утра!",
        "Начните день с позитивного настроя!"
    ],
    "afternoon": [
        "Добрый день! Как проходят ваши дела?",
        "Прекрасный день для великих дел!",
        "Надеемся, ваш день проходит успешно.",
        "Пусть оставшаяся часть дня принесет удачу!",
        "Оставайтесь продуктивными и позитивными!"
    ],
    "evening": [
        "Добрый вечер! Самое время отдохнуть.",
        "Поздний вечер – пора для релаксации.",
        "Как вам сегодняшний вечер?",
        "Оставьте все дела и отдохните.",
        "Вечер – время для душевного отдыха."
    ]
}

# Список мотивирующих цитат
QUOTES = [
    "Всегда верьте в себя, и вы сможете покорить горы.",
    "Каждый день – новый шанс на успех.",
    "Трудности только укрепляют нас.",
    "Будьте упорны и достигнете всего.",
    "Маленькие шаги ведут к великим победам.",
    "Старайтесь и добьетесь результатов.",
    "Ваши усилия приведут к успеху.",
    "Успех приходит к терпеливым.",
    "Упорство и труд все перетрут.",
    "Идите к своей мечте, не останавливайтесь."
]

# Получение сообщения по времени суток
def get_time_message():
    hour = datetime.now().hour
    if 0 <= hour < 6:
        return random.choice(TIME_MESSAGES["night"])
    elif 6 <= hour < 12:
        return random.choice(TIME_MESSAGES["morning"])
    elif 12 <= hour < 18:
        return random.choice(TIME_MESSAGES["afternoon"])
    else:
        return random.choice(TIME_MESSAGES["evening"])

# Получение случайной цитаты
def get_random_quote():
    return random.choice(QUOTES)

def weather(location="Osh"):
    api_key = "a1085c475626c5c58c39d43588398b63"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&lang=ru&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Проверка наличия данных о температуре
        temperature = data['main'].get('temp')
        return temperature
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при подключении к API погоды: {e}")
        return None


def get_weather_message(location="Osh"):
    api_key = "a1085c475626c5c58c39d43588398b63"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&lang=ru&units=metric"
    
    # Словарь сообщений для каждого типа погоды
    weather_messages = {
        "ясно": [
            "Сегодня ясная погода, {temp}°C. Прекрасный день для прогулки!",
            "Солнце светит, и температура {temp}°C. Наслаждайтесь!",
            "Ясное небо и {temp}°C на улице. Отличная погода для отдыха!"
        ],
        "дождь": [
            "Идет дождь и {temp}°C. Возьмите зонт!",
            "Сегодня дождливо, {temp}°C. Одевайтесь теплее!",
            "С дождем на улице и {temp}°C будьте осторожны на дорогах!"
        ],
        "снег": [
            "На улице снег и {temp}°C. Самое время лепить снеговика!",
            "Снегопад и температура {temp}°C. Одевайтесь потеплее!",
            "Идет снег, {temp}°C на улице. Приятно провести время на свежем воздухе!"
        ],
        "облачно": [
            "Небо затянуто облаками, температура {temp}°C.",
            "Сегодня облачно и {temp}°C. Приятного дня!",
            "На улице облачно, {temp}°C. Будьте осторожны!"
        ],
        # Дополнительные погодные условия по умолчанию
        "default": [
            "Сегодня {weather} с температурой {temp}°C. Прекрасный день!",
            "На улице {weather}, {temp}°C. Отличный повод заняться любимым делом!",
            "Погода: {weather}, температура {temp}°C. Удачного дня!"
        ]
    }
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Проверка данных о погоде
        if 'weather' not in data or 'main' not in data:
            print("Ошибка: некорректный формат данных о погоде.")
            return None

        # Извлекаем описание погоды и температуру
        weather_description = data['weather'][0].get('description', 'неизвестно').lower()
        temperature = data['main'].get('temp', 'нет данных')
        
        # Выбираем соответствующее сообщение
        for key in weather_messages.keys():
            if key in weather_description:
                message = random.choice(weather_messages[key])
                break
        else:
            # Если не найдено, используем сообщения по умолчанию
            message = random.choice(weather_messages["default"])
        
        # Возвращаем сообщение с подставленной температурой
        return message.format(temp=round(temperature), weather=weather_description)
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при подключении к API погоды: {e}")
        return None

# Получение случайного сообщения на основе времени, погоды и цитат
def get_dynamic_message():
    # Рандомное переключение между типами сообщений
    options = ["time", "quote", "weather"]
    choice = random.choice(options)
    
    if choice == "time":
        return get_time_message()
    elif choice == "quote":
        return get_random_quote()
    elif choice == "weather":
        weather_message = get_weather_message()
        if weather_message:
            return weather_message
        else:
            return get_random_quote()  # Если погода не загрузилась, используем цитату
