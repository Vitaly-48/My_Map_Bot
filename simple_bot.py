import telebot
import storage
import os
token = os.getenv('1897202859:AAG0mNSPsMQ446m4WQ9IfnwQj3ZHamoUuV8')


def parse_location(message):
    location_parts = message.text.split(' ')[1:]
    if location_parts:
        return ' '.join(location_parts)
    else:
        return ''


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['add'])
def handle_add(message):
    location = parse_location(message)
    if location:
        storage.update_locations(message.chat.id, location)
        bot.send_message(
            message.chat.id, text='Добавлен новый адрес: {}'.format(location))
    else:
        bot.send_message(
            message.chat.id, text='Вы не указали адрес в комманде /add.')


@bot.message_handler(commands=['list'])
def handle_list(message):
    locations = storage.get_locations(message.chat.id)[:10]
    if locations:
        text = '\n'.join(['{}. {}'.format(index + 1, loc)
                          for index, loc in enumerate(locations)])
    else:
        text = 'У вас ещё нет добавленных адресов. Используйте комманду /add, чтобы добавлять локации.'
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=['reset'])
def handle_reset(message):
    storage.reset_locations(message.chat.id)
    bot.send_message(message.chat.id, text='Ваши данные удалены')


@bot.message_handler()
def handle_help(message):
    bot.send_message(message.chat.id, text='''
    Это демонстрация базового бота для добавления локаций. \n
Он позволяет выполнять две команды: \n
/add Мясницкая, 12 должен сохранить новый адрес в список сохраненных локаций \n
/list должен вернуть список из 10 последних локаций \n
/reset позволяет пользователю удалить все его добавленны локации (помним про GDPR) \n
    ''')


bot.polling()
