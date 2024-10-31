# context_processors.py
from .utils import get_temperature  # Подключите функцию получения температуры

def weather_data(request):
    temperature = get_temperature("Moscow")  # Замените "Moscow" на нужное вам местоположение
    return {
        "temperature": temperature
    }
