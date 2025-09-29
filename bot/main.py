import telebot
import requests

bot = telebot.TeleBot('8358485313:AAFzOy4z6_icHsshiuJYwt2rb8L4idjUnJg')
API = '7307ddf3c705c122b60c8cd7f661b014'

def fetch_weather(city):
    """
    Получает данные о погоде для указанного города через OpenWeatherMap API.
    
    Args:
        city (str): Название города.
        
    Returns:
        dict or None: JSON с данными о погоде, если запрос успешен, иначе None.
    """
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric&lang=ru'
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    return None

def format_weather_response(city, data):
    """
    Формирует текст ответа для пользователя на основе данных о погоде.
    
    Args:
        city (str): Название города.
        data (dict): JSON с данными о погоде.
        
    Returns:
        tuple: (текст ответа (str), описание погоды (str), температура (int))
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
    
    Args:
        description (str): Описание погоды.
        temp (int): Температура воздуха.
        
    Returns:
        str: Путь к изображению.
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
    отправляет погодные данные и соответствующее фото.
    """
    city = message.text.strip()
    data = fetch_weather(city)
    if data:
        answer, description, temp = format_weather_response(city, data)
        image = select_image(description, temp)

        with open(image, "rb") as file:
            bot.send_photo(message.chat.id, file, caption=answer)
    else:
        bot.reply_to(
            message,
            "😔 Не удалось найти такой город. Проверь правильность написания."
        )

bot.polling(none_stop=True)
