import config
import telebot
import lesgaft_bot_db


bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, *имя*, напиши номер своей группы')
    
    print(message.text)

@bot.message_handler(content_types=["text"])
def main_func(message):
    if message.text == 'Расписание':
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        key_week = telebot.types.InlineKeyboardButton(text='Неделя', callback_data='week')
        inline_keyboard.add(key_week)
        key_today = telebot.types.InlineKeyboardButton(text='Сегодня', callback_data='today')
        inline_keyboard.add(key_today)
        key_now = telebot.types.InlineKeyboardButton(text='Сейчас', callback_data='now')
        inline_keyboard.add(key_now)
        bot.send_message(message.from_user.id, 'Теперь выбери что-нибудь', reply_markup=inline_keyboard)
    try:
        number_of_group = int(message.text)
        student_info = [(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.date, number_of_group)]
        lesgaft_bot_db.starting_insert_data(student_info)

        main_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        main_keyboard.row('Расписание')

        bot.send_message(message.chat.id, 'Отлично, теперь продолжим', reply_markup=main_keyboard)
        print(message.text)
    except Exception:
        remove_obj = telebot.types.ReplyKeyboardRemove(True)
        bot.send_message(message.chat.id, 'Это что-то не то. Введи номер группы числом', reply_markup = remove_obj)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'week':
        #bot.send_message(message.chat.id, '#qwe')
        print('week')
    elif call.data == 'today':
        print('today')
    elif call.data == 'now':
        print('now')
    

if __name__ == '__main__':
    bot.polling(none_stop=True)
