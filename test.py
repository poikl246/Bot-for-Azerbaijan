import telebot

with open('config/config.txt') as conf:
    bot_api = (conf.readline())[:-1]
    admin_l = conf.readlines()
    admin_list = []
    for admin in admin_l[:-1]:
        admin_list.append(admin[:-1])

    if list(admin_l[-1])[-1] != '\n':
        admin_list.append(int(admin_l[-1]))
    else:
        admin_list.append(int((admin_l[-1])[:-1]))
    print(admin_list)

bot = telebot.TeleBot(bot_api)
token = bot_api
print('Connect')

service = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

service.row(f'156468')

bot.send_message(964296210, '8453120', reply_markup=service)