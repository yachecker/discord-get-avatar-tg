from bs4 import BeautifulSoup as BS
import requests
import telebot
from telebot import types
token = '5395944286:AAHYK26CIWrE9FrAJe5YE0_pYfef9NA4QoM'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def hello(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('💎Получить данные')
    button2 = types.KeyboardButton('🛡Информация')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, text='Привет', reply_markup=keyboard)


data = {'size': 2048}


@bot.message_handler(content_types=['text'])
def text(message):
    if(message.text == '💎Получить данные'):
        msg = bot.send_message(message.chat.id, "Введите ID пользователя:")
        bot.register_next_step_handler(msg, get_user_id)
    elif message.text == '🛡Информация':
        msg = bot.send_message(message.chat.id, "Информация о боте:\nБот находит аватарку пользователя в дискорде по введеному ID.\nID искомого пользователя можно найти нажав правую кнопку мыши по пользователю, после нужно нажать на конпку \"Копировать ID\".")
    else:
        bot.send_message(message.chat.id, "Я не могу обработать что вы написали, нажмите кнопку 🛡Информация, чтобы узнать о функционале бота.")

def get_user_id(message):
    if message.text == '🛡Информация':
        bot.send_message(message.chat.id, 'Информация о боте:\nБот находит аватарку пользователя в дискорде по введеному ID.\nID искомого пользователя можно найти нажав правую кнопку мыши по пользователю, после нужно нажать на конпку \"Копировать ID\".')
    elif len(message.text) < 18:
        msg = bot.send_message(message.chat.id,'Введите действительный ID пользователя')
        bot.register_next_step_handler(msg, get_user_id)
    else:
        user_id = message.text
        url = 'https://discord-avatar.com/en/user/'+str(user_id)
        html = requests.get(url, data)
        soup = BS(html.text)
        error = soup.find('h1', {"class":"h2 text-center"})
        if error.text == "error.notfound":
            msg = bot.send_message(message.chat.id, "Пользователь не найден")
            bot.register_next_step_handler(msg,get_user_id)
        else:
            user_id = message.text
            url = 'https://discord-avatar.com/en/user/'+str(user_id)
            html = requests.get(url, data)
            soup = BS(html.text)
            image = soup.find('img')
            name = soup.find('li', {"class": "list-group-item active"}
                            ).text.replace(" ", "").replace("\n", "")
            bot.send_photo(message.chat.id,
                        image['src'], caption=f'Пользователь: {name}')


bot.polling()
