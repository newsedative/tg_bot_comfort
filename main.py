import telebot
from telebot import types
from for_db import BotDB
import requests
from additions import add_sticker, add_music
from api.weather import get_weather
import time
from api.for_affirmation import random_aff

BOT_TOKEN = ' '
bot = telebot.TeleBot(BOT_TOKEN)


def unclear(mes):
    bot.send_message(mes.from_user.id, 'idk')


# запуск бота, приветственное сообщение
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "<b>✨Привет, я бот, который сохранит твоё ментальное здоровье! ✨</b>\n"
                                           "\n"
                                           "Здесь ты найдёшь: аффирмации, дыхательную гимнастику,"
                                           "звуки природы и музыку для медитации.\n"
                                           "\n"
                                           "Чтобы узнать, что бот умеет напиши слеш /\n"
                                           "Чтобы перейти к возможностям бота \n"
                                           "/commands\n"
                                           "Если есть вопросы пиши /help", parse_mode='html')
    bot.send_sticker(message.from_user.id, add_sticker())
    db_cr = BotDB()
    user_id = message.from_user.id
    # проверка регистрации пользователя
    if not db_cr.check(user_id):
        db_cr.add_us(user_id)
        bot.send_message(message.from_user.id, "регистрация выполнена")
    else:
        bot.send_message(message.from_user.id, "вход выполнен")
    msg = bot.send_message(message.from_user.id, "напишите в каком вы городе")
    bot.register_next_step_handler(msg, city)


# подсказать пользователю погоду
def city(message):
    city_w = get_weather(message.text)
    bot.send_message(message.from_user.id, city_w)


# команда с терминами
@bot.message_handler(commands=['what_is'])
def what(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Что такое медитация?', url="https://clck.ru/bArjy")
    btn2 = types.InlineKeyboardButton('Что такое аффирмация?', url="https://clck.ru/L6Jsc")
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, 'Здесь вы узнаете 👇', reply_markup=markup)


# если пользователю нужна помощь
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_sticker(message.from_user.id, add_sticker())
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('ВКонтакте ⚡️', url='vk.com/dmashinova'))
    bot.send_message(message.from_user.id, '1) Чтобы посмотреть все команды и узнать, что они делают напишите слэш /'
                                           '\n'
                                           '2) Чтобы перейти к возможностям бота напишите /commands'
                                           '\n'
                                           '3) Пишите сюда, если что-то не работает👇', reply_markup=markup)


# меню с возможностями бота
@bot.message_handler(commands=['commands'])
def commands(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    btn_med = types.KeyboardButton('☀️Выбрать часть суток')
    btn_mus = types.KeyboardButton('🎧Музыка')
    markup.add(btn_med, btn_mus)
    msg = bot.send_message(message.from_user.id, 'Выбирайте', reply_markup=markup)
    bot.register_next_step_handler(msg, selection)


def selection(message):
    if message.text == '☀️Выбрать часть суток':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🌇утро/день')
        btn2 = types.KeyboardButton('🌃вечер/ночь')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, 'выбирайте', reply_markup=markup)
    elif message.text == '🎧Музыка':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('звуки природы')
        btn2 = types.KeyboardButton('загрузить свою музыку')
        markup.add(btn1, btn2)
        msg = bot.send_message(message.from_user.id, 'Любая музыка влияет на дыхание, пульс, '
                                               'кровяное давление и энергетику. Музыка может '
                                               'снимать стресс и повышать иммунитет, поднимать '
                                               'силу духа, вдохновить на творчество.', reply_markup=markup)
        bot.register_next_step_handler(msg, music)
    else:
        unclear(message)


# функции к кнопке 'Музыка'
def music(message):
    if message.text == 'загрузить свою музыку':
        bot.send_message(message.from_user.id, 'отправьте файл в формате mp3')
    elif message.text == 'звуки природы':
        audio = open(f'music_of_nature/{add_music()}', 'rb')
        bot.send_audio(message.from_user.id, audio)


# обработка кнопок
@bot.message_handler(func=lambda m: True)
def all_mes(message):
    if message.text == '🌇утро/день':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        key_af = types.InlineKeyboardButton(text='аффирмация на день', callback_data='affirmation')
        key_pr = types.InlineKeyboardButton(text='дыхательная практика', callback_data='practica')
        keyboard.add(key_af, key_pr)
        bot.send_message(message.from_user.id, 'предлагаем вам взбодрится', reply_markup=keyboard)
    elif message.text == '🌃вечер/ночь':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        key_af = types.InlineKeyboardButton(text='медитация', callback_data='meditation')
        key_pr = types.InlineKeyboardButton(text='дыхательная практика', callback_data='practica')
        keyboard.add(key_af, key_pr)
        bot.send_message(message.from_user.id, 'предлагаем вам расслабиться', reply_markup=keyboard)
    else:
        unclear(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_work(call):
    if call.data == 'affirmation':
        bot.send_message(call.message.chat.id, f'🪴Аффирмация'
                                               '\n'
                                               '\n'
                                               'Повторите аффирмацию несколько раз. Чтобы ощутить эффект от аффирмаций,'
                                               ' проговаривайте их вслух каждое утро. 👇')
        bot.send_message(call.message.chat.id, random_aff())
    elif call.data == 'meditation':
        bot.send_message(call.message.chat.id, 'вот medita')
    elif call.data == 'practica':
        bot.send_message(call.message.chat.id, 'Дыхательная практика: Сядьте или лягте, расслабьте мышцы рук, ног, '
                                               'лица и верхние мышцы груди. '
                                               '\n'
                                               '\n'
                                               'Я пишу вы делаете')
        for i in range(4):
            bot.send_message(call.message.chat.id, 'Вдыхайте')
            time.sleep(4)
            bot.send_message(call.message.chat.id, 'Выдыхайте')
            time.sleep(4)
        bot.send_message(call.message.chat.id, 'Закончили')
    else:
        bot.send_message(call.message.chat.id, 'idk')


def breathing(message):
    bot.send_message(message.from_user.id, 'gdgfhhjhtrgerwer')


# обработка аудио от пользователя
@bot.message_handler(content_types='audio')
def handle_docs_photo(message):
    file_info = bot.get_file(message.audio.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(BOT_TOKEN, file_info.file_path))

    msg = bot.send_message(message.from_user.id, 'напишите название файла')
    bot.register_next_step_handler(msg, take_name, file)


def take_name(message, fi):
    music = message.text
    with open(f'user_files/{music}.mp3', 'wb') as f:
        f.write(fi.content)
    bot.send_message(message.from_user.id, 'ваша музыка загружена')


if __name__ == '__main__':  # чтобы код выполнялся только при запуске в виде сценария, а не при импорте модуля
    try:
        bot.polling(none_stop=True)  # запуск бота
    except Exception as e:
        print(e)
        time.sleep(15)