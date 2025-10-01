import telebot
import requests

"""
Погодный бот weathrubot.
Функционал:
- принимает название города от пользователя,
- получает данные о погоде через OpenWeatherMap API,
- отправляет пользователю температуру, описание и картинку в зависимости от погоды.
"""

bot = telebot.TeleBot('Сюда токен')
API = '7307ddf3c705c122b60c8cd7f661b014'

def collect_data(city):
    """
    Получает текущие погодные данные для указанного города через OpenWeatherMap API.
    """
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric&lang=ru'
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    return None

def send_weather(city, data):
    """
    Обработчик сообщений.
    Принимает название города, делает запрос к API OpenWeatherMap,
    получает текущие данные о погоде и отправляет пользователю:
    - Температуру
    - Ощущаемую температуру
    - Описание погоды
    Также прикладывает соответствующую картинку котеночка в зависимости от погоды.
    """
    temp = round(data["main"]["temp"])
    feels = round(data["main"]["feels_like"])
    description = data["weather"][0]["description"].capitalize()
    answer = (
        f"Город🌆: {city.title()}\n"
        f"Температура🌡: {temp}°C\n"
        f"Ощущается как👟: {feels}°C\n"
        f"Погода🌦: {description}"
    )
    return answer, description, temp

def select_image(description, temp):
    """
    Выбирает путь к изображению с котенком в зависимости от погоды.
    """
    desc_lower = description.lower()
    if "дожд" in desc_lower:
        return "C:/Labaratorki/telegram-bot/bot/images/rainy.jpg"
    elif "пасмур" in desc_lower or "облач" in desc_lower:
        return "C:/Labaratorki/telegram-bot/bot/images/cloudy.jpg"
    elif temp < 10:
        return "C:/Labaratorki/telegram-bot/bot/images/cold.png"
    else:
        return "C:/Labaratorki/telegram-bot/bot/images/sunny.jpg"

@bot.message_handler(commands=['start'])
def start(message):
    """
    Обработчик команды /start. Отправляет приветствие и инструкцию пользователю.
    """
    bot.send_message(
        message.chat.id,
        'Привет, я погодный бот - weathrubot! Напиши название города, и я покажу твою погоду 🌤'
    )

@bot.message_handler(content_types=['text'])
def get_weather(message):
    """
    Обработчик текстовых сообщений - принимает название города, запрашивает погоду,
    отправляет погодные данные и соответствующее фото котенка.
    """
    city = message.text.strip()
    data = collect_data(city)
    if data:
        answer, description, temp = send_weather(city, data)
        image = select_image(description, temp)

        with open(image, "rb") as file:
            bot.send_photo(message.chat.id, file, caption=answer)
    else:
        bot.reply_to(
            message,
            "😔 Не удалось найти такой город. Проверь правильность написания."
        )

"""
Запуск бота.
Работает в бесконечном цикле,благодаря чему бот не заканчивает работу и обрабатывает входящие сообщения.
"""
bot.polling(none_stop=True)
