import telebot
import requests

bot = telebot.TeleBot('8358485313:AAFzOy4z6_icHsshiuJYwt2rb8L4idjUnJg')
API = '7307ddf3c705c122b60c8cd7f661b014'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, я погодный бот - weathrubot! Напиши название города, и я покажу твою погоду 🌤')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip()
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric&lang=ru'

    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        temp = round(data["main"]["temp"])
        feels = round(data["main"]["feels_like"])
        description = data["weather"][0]["description"].capitalize()

        answer = (f"Город🌆: {city.title()}\n"
                f"Температура🌡: {temp}°C\n"
                f"Ощущается как👟: {feels}°C\n"
                f"Погода🌦: {description}")

        if "дожд" in description.lower():
            image = "C:/Labaratorki/telegram-bot/venv/images/rainy.jpg"
        elif "пасмур" in description.lower() or "облач" in description.lower():
            image = "C:/Labaratorki/telegram-bot/venv/images/cloudy.jpg"
        elif temp < 10:
            image = "C:/Labaratorki/telegram-bot/venv/images/cold.png"
        else:
            image = "C:/Labaratorki/telegram-bot/venv/images/sunny.jpg"

        with open(image, "rb") as file:
            bot.send_photo(message.chat.id, file, caption=answer)

    else:
        bot.reply_to(message, "😔 Не удалось найти такой город. Проверь правильность написания.")

bot.polling(none_stop=True)