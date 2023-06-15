import telebot
import os
from PIL import Image, ImageDraw, ImageFont
from telebot import types

os.system('clear')

current_dir = os.path.dirname(os.path.abspath(__file__))
ryan_image = os.path.join(current_dir, "ryan.jpg")
ryansad_image = os.path.join(current_dir, "ryansad.jpg")
ryanhappy_image = os.path.join(current_dir, "ryanhappy.jpg")
font_path = os.path.join(current_dir, "OpenSans-Bold.ttf")

# Замените 'YOUR_TOKEN' на ваш токен API
bot = telebot.TeleBot('5972890359:AAFflccB3LFr6hGoShrOBZ0C20AA8tDJ29Y')

keyboard = types.ReplyKeyboardMarkup(row_width=2)
button_ryan = types.KeyboardButton('Райан')
button_ryansad = types.KeyboardButton('Грустный Райан')
button_ryanhappy = types.KeyboardButton('Веселый Райан')

keyboard.add(button_ryan, button_ryansad, button_ryanhappy)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Кинь мне текст, и я помещу его на картинке Райана Гослинга)",
        reply_markup=keyboard  # Добавление клавиатуры к сообщению
    )

@bot.message_handler(func=lambda message: message.text == 'Райан')
def handle_ryan(message):
    global image_path
    image_path = ryan_image
    bot.send_message(message.chat.id, "Выбрана картинка 'Райан'")

@bot.message_handler(func=lambda message: message.text == 'Грустный Райан')
def handle_ryansad(message):
    global image_path
    image_path = ryansad_image
    bot.send_message(message.chat.id, "Выбрана картинка 'Грустный Райан'")

@bot.message_handler(func=lambda message: message.text == 'Веселый Райан')
def handle_ryanhappy(message):
    global image_path
    image_path = ryanhappy_image
    bot.send_message(message.chat.id, "Выбрана картинка 'Веселый Райан'")

def load_prohibited_words():
    words = []
    with open("words.txt", "r") as file:
        for line in file:
            word = line.strip()
            words.append(word)
    return words

def load_mother_words():
    mother_words = []
    with open("motherwords.txt", "r") as file:
        for line in file:
            word = line.strip()
            mother_words.append(word)
    return mother_words

def add_text_to_image(image_path, text):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, 40)

    # Установка координат и цвета для текста на картинке
    x = 830
    y = 200
    text_color = (255, 255, 255)

    if len(text) > 30:
        # Разделение текста на строки
        lenwords = text.split()
        lines = []
        current_line = ""
        for lenword in lenwords:
            if len(current_line + lenword) <= 15:
                current_line += lenword + " "
            else:
                lines.append(current_line)
                current_line = lenword + " "
        lines.append(current_line)

        # Добавление текста на картинку по строкам
        for i, line in enumerate(lines):
            draw.text((x, y + i*40), line, fill=text_color, font=font)
    else:
        # Добавление текста без переноса
        draw.text((x, y), text, fill=text_color, font=font)

    # Сохранение измененной картинки
    output_path = "output.jpg"
    image.save(output_path)
    return output_path

@bot.message_handler(func=lambda message: True)
def process_message(message):
    global image_path  # Добавлено глобальное объявление переменной
    chat_id = message.chat.id
    message_text = message.text

    print(f"Сообщение от пользователя (ID чата {chat_id}): {message_text}")
    with open("messages.txt", "a") as file:
        file.write(f"ID чата {chat_id}: {message_text}\n")

    prohibited_words = load_prohibited_words()
    for word in prohibited_words:
        if word in message_text.lower():
            bot.send_message(chat_id, "Нет, это ты " + word + "!")
            return

    joke_mother_words = load_mother_words()
    for word in joke_mother_words:
        if word in message_text.lower():
            bot.send_message(chat_id, "Маму не трогай!")
            return
    # Добавление текста на изображение
    output_image_path = add_text_to_image(image_path, message_text)
    # Отправка измененной картинки пользователю
    with open(output_image_path, "rb") as image_file:
        bot.send_photo(chat_id, image_file)

bot.polling()