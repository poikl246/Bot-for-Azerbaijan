import json
import os
import time

import requests
import telebot
from telebot import types
import csv
from threading import Thread

templates = {}

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

if not os.path.exists('data/data.json'):
    templates = {}
    with open("data/data.json", "w", encoding='utf-8') as file:
        json.dump(templates, file, indent=4, ensure_ascii=False)

else:
    with open("data/data.json", 'r', encoding='utf-8') as f:
        templates = json.load(f)



def vopros_input():
    def variant_otvet(row):
        data_fins = []
        for i in range(1, 31):
            if row[f'{i}'] != '':
                data_fins.append(row[f'{i}'])
            else:
                break

        return data_fins

    data = {}

    with open("config/Suallar1.csv", 'r', encoding='utf-8') as r_file:
        # Создаем объект DictReader, указываем символ-разделитель ","
        file_reader = csv.DictReader(r_file, delimiter=";")
        # Счетчик для подсчета количества строк и вывода заголовков столбцов
        count = 1
        # Считывание данных из CSV файла
        for row in file_reader:
            data[count] = {
                'N': row['N'],
                'Questions': row['Questions'],
                'Type': row['Type'],
                "Caunt": row['Caunt'],
                'answer': f'{variant_otvet(row=row)}'

            }
            count += 1

    data1 = {}
    with open("config/input.csv", 'r', encoding='utf-8') as r_file:
        # Создаем объект DictReader, указываем символ-разделитель ","
        file_reader = csv.DictReader(r_file, delimiter=";")
        # Счетчик для подсчета количества строк и вывода заголовков столбцов
        count = 1
        # Считывание данных из CSV файла
        # print(file_reader)
        for row in file_reader:
            # print(row)
            data1[count] = {
                'agreement': row['agreement'],
                'Error': row['Error'],
                'Hot lines': row['Hot lines'],
                "Question": row['Question'],
                'Final message': row['Final message']

            }
            count += 1



    return data, data1

Global_vopros, One_data = vopros_input()



def vopros_vi(bot, id_pade, Namber):
    Namber = int(Namber)


    if Global_vopros[Namber]['Type'] == 'text':
        bot.send_message(id_pade, Global_vopros[Namber]['Questions'])

    elif Global_vopros[Namber]['Type'] == 'variable':
        service = telebot.types.ReplyKeyboardMarkup(True, True)


        for vopros_data_ in (Global_vopros[Namber]['answer'].replace("'", "").replace("[", '').replace(']', '').split(',')):
            try:
                service.row(f'{vopros_data_}')
            except:
                break
        bot.send_message(id_pade, Global_vopros[Namber]['Questions'], reply_markup=service)


    elif Global_vopros[Namber]['Type'] == 'batton':
        if Namber == 5:
            button_Cins(id_page=id_pade, vopros=Global_vopros[Namber]['Questions'])
        elif Namber == 1:
            markup = types.InlineKeyboardMarkup(row_width=3)
            # for i in range(1, 18+1):
            #     item2 = types.InlineKeyboardButton('Пока', callback_data=f'{i}')
            #     markup.add(item2)
            # i = 1
            item1 = types.InlineKeyboardButton('Ərizə', callback_data=f'Ərizə')
            item2 = types.InlineKeyboardButton('Təklif', callback_data=f'Təklif')
            item3 = types.InlineKeyboardButton('Şikayət', callback_data=f'Şikayət')
            markup.add(item1, item2, item3)

            bot.send_message(id_pade, f"{Global_vopros[Namber]['Questions']}", reply_markup=markup)
        elif Namber == 10:
            markup = types.InlineKeyboardMarkup(row_width=3)
            # for i in range(1, 18+1):
            #     item2 = types.InlineKeyboardButton('Пока', callback_data=f'{i}')
            #     markup.add(item2)
            # i = 1
            item1 = types.InlineKeyboardButton('Fərdi', callback_data=f'Fərdi')
            item2 = types.InlineKeyboardButton('Kollektiv', callback_data=f'Kollektiv')
            # item3 = types.InlineKeyboardButton('Şikayət', callback_data=f'Şikayət')
            markup.add(item1, item2)

            bot.send_message(id_pade, f"{Global_vopros[Namber]['Questions']}", reply_markup=markup)
        elif Namber == 13:
            markup = types.InlineKeyboardMarkup(row_width=3)
            # for i in range(1, 18+1):
            #     item2 = types.InlineKeyboardButton('Пока', callback_data=f'{i}')
            #     markup.add(item2)
            # i = 1
            item1 = types.InlineKeyboardButton('Bəli', callback_data=f'Yes')
            item2 = types.InlineKeyboardButton('Xeyr', callback_data=f'No')
            # item3 = types.InlineKeyboardButton('Şikayət', callback_data=f'Şikayət')
            markup.add(item1, item2)

            bot.send_message(id_pade, f"{Global_vopros[Namber]['Questions']}", reply_markup=markup)



def Save_data_exel(id_page, Global_vopros):
    with open("data/data.json", 'r', encoding='utf-8') as f:
        templates = json.load(f)
    print('Save data in csv')
    templates[f"{id_page}"]['Number'] = '0'
    with open("data/data.json", "w", encoding='utf-8') as file:
        json.dump(templates, file, indent=4, ensure_ascii=False)

    def new_file(Global_vopros):
        # gho = 10

        file_list = ['№', 'id']
        for gho in range(1, 14):
            text = str(Global_vopros[gho]['Questions'])
            file_list.append(text)
        with open('Output_csv/Data.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows([file_list])


        with open('Output_csv/Data.txt', 'w', encoding='utf-8') as file:
            file.write('0')

    if not os.path.exists('Output_csv/Data.csv'):
        new_file(Global_vopros)

    with open('Output_csv/Data.txt', 'r') as file:
        namber = int(file.readline()) + 1


    if namber > 100000:
        for admin_bot in admin_list:
            bot.send_document(admin_bot, open(r'Output_csv/Data.csv', 'rb'))
        os.rename('Output_csv/Data.csv', f'Output_csv/Data_{time.time()}.csv')
        new_file(Global_vopros)
        namber = 1

    file_list = [
        namber,
        templates[f"{id_page}"]['id'],
        templates[f"{id_page}"]['of_appeal'],
        templates[f"{id_page}"]['FIO'],
        templates[f"{id_page}"]['3'],
        templates[f"{id_page}"]['4'],
        templates[f"{id_page}"]['gender'],
        templates[f"{id_page}"]['6'],
        templates[f"{id_page}"]['7'],
        templates[f"{id_page}"]['8'],
        templates[f"{id_page}"]['9'],
        templates[f"{id_page}"]['123963appeal'],
        templates[f"{id_page}"]['11'],
        templates[f"{id_page}"]['12'],
        templates[f"{id_page}"]['file']]

    with open('Output_csv/Data.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows([file_list])
    # print(str(templates[f'{id_page}']['FIO']))
    bot.send_message(int(templates[f'{id_page}']['id']), f"{str(templates[f'{id_page}']['FIO']).split(' ')[0]} {One_data[1]['Final message']}")

    del templates[f"{id_page}"]
    with open("data/data.json", "w", encoding='utf-8') as file:
        json.dump(templates, file, indent=4, ensure_ascii=False)

    with open('Output_csv/Data.txt', 'w') as file:
        file.write(str(namber))

    selfmyself1(id_page=id_page)





    #
def button_Cins(id_page, vopros):

    markup = types.InlineKeyboardMarkup(row_width=3)
    # for i in range(1, 18+1):
    #     item2 = types.InlineKeyboardButton('Пока', callback_data=f'{i}')
    #     markup.add(item2)
    # i = 1
    item1 = types.InlineKeyboardButton('👩🏻 Qadın', callback_data='Qadın')
    item2 = types.InlineKeyboardButton('👨🏻 Kişi', callback_data=f'Kişi')

    markup.add(item1, item2)


    bot.send_message(id_page, vopros, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        with open("data/data.json", 'r', encoding='utf-8') as f:
            templates = json.load(f)

        if call.data == 'Qadın':

            templates[f'{call.message.chat.id}']['gender'] = 'Qadın'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Qadın')
            templates[f"{call.message.chat.id}"]['Number'] = str(
                int(templates[f"{call.message.chat.id}"]['Number']) + 1)


        elif call.data == 'Kişi':
            templates[f'{call.message.chat.id}']['gender'] = 'Kişi'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Kişi')
            templates[f"{call.message.chat.id}"]['Number'] = str(
                int(templates[f"{call.message.chat.id}"]['Number']) + 1)

        elif call.data == 'Ərizə':
            templates[f'{call.message.chat.id}']['of_appeal'] = 'Ərizə'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Ərizə')
            templates[f"{call.message.chat.id}"]['Number'] = str(
                int(templates[f"{call.message.chat.id}"]['Number']) + 1)

        elif call.data == 'Təklif':
            templates[f'{call.message.chat.id}']['of_appeal'] = 'Təklif'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Təklif')
            templates[f"{call.message.chat.id}"]['Number'] = str(int(templates[f"{call.message.chat.id}"]['Number']) + 1)

        elif call.data == 'Şikayət':
            templates[f'{call.message.chat.id}']['of_appeal'] = 'Şikayət'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Şikayət')
            templates[f"{call.message.chat.id}"]['Number'] = str(int(templates[f"{call.message.chat.id}"]['Number']) + 1)

        elif call.data == 'Fərdi':
            templates[f'{call.message.chat.id}']['123963appeal'] = 'Fərdi'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Fərdi')
            templates[f"{call.message.chat.id}"]['Number'] = str(int(templates[f"{call.message.chat.id}"]['Number']) + 1)
        elif call.data == 'Kollektiv':
            templates[f'{call.message.chat.id}']['123963appeal'] = 'Kollektiv'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f"✅ {str(templates[f'{call.message.chat.id}']['FIO']).split(' ')[0]} xahiş olunur digər subyektlərin ad, soyad, ata adı və əlaqə nömrələrini ardıcıllıqla yazasınız")
            templates[f"{call.message.chat.id}"]['Number'] = '!!!'
            time.sleep(0.5)

            with open("data/data.json", "w", encoding='utf-8') as file:
                json.dump(templates, file, indent=4, ensure_ascii=False)


            return 1


        elif call.data == 'Yes':
            templates[f'{call.message.chat.id}']['file'] = 'Bəli'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Bəli")
            # templates[f"{call.message.chat.id}"]['Number'] = '2'
            with open("data/data.json", "w", encoding='utf-8') as file:
                json.dump(templates, file, indent=4, ensure_ascii=False)
            Save_data_exel(id_page=call.message.chat.id, Global_vopros=Global_vopros)
            return 1
        elif call.data == 'No':
            templates[f'{call.message.chat.id}']['file'] = 'Xeyr'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Xeyr')
            with open("data/data.json", "w", encoding='utf-8') as file:
                json.dump(templates, file, indent=4, ensure_ascii=False)
            Save_data_exel(id_page=call.message.chat.id, Global_vopros=Global_vopros)
            return 1
            # templates[f"{call.message.chat.id}"]['Number'] = str(
            #     int(templates[f"{call.message.chat.id}"]['Number']) + 1)

        elif call.data == 'Razıyam':
            selfmyself(message=call)
            return 1

        elif call.data == 'Telephone':
            bot.send_message(call.message.chat.id, One_data[1]['Hot lines'])
            return 1

        elif call.data == 'URL_global':

            markup = types.InlineKeyboardMarkup(row_width=3)
            # for i in range(1, 18+1):
            #     item2 = types.InlineKeyboardButton('Пока', callback_data=f'{i}')
            #     markup.add(item2)
            # i = 1
            item1 = types.InlineKeyboardButton('Facebook', url='https://m.facebook.com/meclisinfo')
            item2 = types.InlineKeyboardButton('Instagram', url='https://instagram.com/meclis.info')
            item3 = types.InlineKeyboardButton('TikTok', url='https://www.tiktok.com/@meclis.info')
            item4 = types.InlineKeyboardButton('YouTube', url='https://youtube.com/channel/UC_te1GjfOAg4eyBnhVDZvbg')
            item5 = types.InlineKeyboardButton('🌐 Meclis', url='https://meclis.info/')
            markup.add(item1, item2, item3, item4, item5)

            bot.send_message(call.message.chat.id, 'Bizi izlə', reply_markup=markup)
            return 1



        elif call.data == 'Greedy_global':
            templates[f"{call.message.chat.id}"] = {
                "id": f"{call.message.chat.id}",
                "FIO": "",
                "Number": "1"
            }

        with open("data/data.json", "w", encoding='utf-8') as file:
            json.dump(templates, file, indent=4, ensure_ascii=False)
        vopros_vi(bot, call.message.chat.id, templates[f'{call.message.chat.id}']['Number'])

@bot.message_handler(commands=['restart'])
def selfmyself(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    # for i in range(1, 18+1):
    #     item2 = types.InlineKeyboardButton('Пока', callback_data=f'{i}')
    #     markup.add(item2)
    # i = 1
    item1 = types.InlineKeyboardButton('📢 Müraciətini göndər', callback_data='Greedy_global')
    item2 = types.InlineKeyboardButton('☎️ Qaynar xətlər', callback_data=f'Telephone')
    item3 = types.InlineKeyboardButton('🤔 Sual ver', url=f"https://t.me/{str(One_data[1]['Question'])}")
    item4 = types.InlineKeyboardButton('🔗 Bizi izlə', callback_data=f'URL_global')

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.from_user.id, 'Siz əsas menyudasınız. Seçim edin', reply_markup=markup)


def selfmyself1(id_page):
    markup = types.InlineKeyboardMarkup(row_width=2)
    # for i in range(1, 18+1):
    #     item2 = types.InlineKeyboardButton('Пока', callback_data=f'{i}')
    #     markup.add(item2)
    # i = 1
    item1 = types.InlineKeyboardButton('📢 Müraciətini göndər', callback_data='Greedy_global')
    item2 = types.InlineKeyboardButton('☎️ Qaynar xətlər', callback_data=f'Telephone')
    item3 = types.InlineKeyboardButton('🤔 Sual ver', url=f"https://t.me/{str(One_data[1]['Question'])}")
    item4 = types.InlineKeyboardButton('🔗 Bizi izlə', callback_data=f'URL_global')

    markup.add(item1, item2, item3, item4)

    bot.send_message(id_page, 'Siz əsas menyudasınız. Seçim edin', reply_markup=markup)



@bot.message_handler(commands=['start'])
def start_bot(message):
    markup = types.InlineKeyboardMarkup(row_width=3)

    item1 = types.InlineKeyboardButton(f'Razıyam ✅', callback_data=f'Razıyam')
    # item2 = types.InlineKeyboardButton('Kollektiv', callback_data=f'Kollektiv')
    # item3 = types.InlineKeyboardButton('Şikayət', callback_data=f'Şikayət')
    markup.add(item1)
    bot.send_message(message.from_user.id, f'{One_data[1]["agreement"]}', reply_markup=markup)


@bot.message_handler(commands=['data_output'])
def data_out(message):

    if int(message.from_user.id) in admin_list:
        if os.path.exists(r'Output_csv/Data.csv'):
            bot.send_document(message.from_user.id, open(r'Output_csv/Data.csv', 'rb'))
        else:
            bot.send_message(message.from_user.id, 'Until the file is created')


@bot.message_handler(content_types=['text'])
def texl_loyder(message):

    try:
        with open("data/data.json", 'r', encoding='utf-8') as f:
            templates = json.load(f)


        if templates[f"{message.from_user.id}"]['Number'] == '2':
            templates[f"{message.from_user.id}"]['FIO'] = message.text
            templates[f"{message.from_user.id}"]['Number'] = '3'

        elif templates[f"{message.from_user.id}"]['Number'] == '0':
            templates[f"{message.from_user.id}"]['Number'] = '1'

        elif templates[f"{message.from_user.id}"]['Number'] == "!!!":
            templates[f'{message.from_user.id}']['123963appeal'] = message.text
            templates[f"{message.from_user.id}"]['Number'] = '11'
            with open("data/data.json", "w", encoding='utf-8') as file:
                json.dump(templates, file, indent=4, ensure_ascii=False)
            # vopros_vi(bot, message.from_user.id, templates[f'{message.from_user.id}']['Number'])
        else:
            if templates[f"{message.from_user.id}"]['Number'] == '3':
                for bykva in list(str(message.text)):
                    if not bykva in '1234567890., ':
                        print(f'{bykva} - неверно')
                        bot.send_message(message.from_user.id, f"{One_data[1]['Error']}")
                        return 1



                templates[f"{message.from_user.id}"][templates[f"{message.from_user.id}"]['Number']] = message.text
                templates[f"{message.from_user.id}"]['Number'] = str(int(templates[f"{message.from_user.id}"]['Number']) + 1)

            elif templates[f"{message.from_user.id}"]['Number'] == '4':
                caunt_local = 0
                for bykva in list(str(message.text)):
                    if not bykva in '1234567890 ':
                        print(f'{bykva} - неверно')
                        bot.send_message(message.from_user.id, f"{One_data[1]['Error']}")
                        return 1
                    elif bykva in '1234567890':
                        caunt_local += 1

                if caunt_local < 9:
                    bot.send_message(message.from_user.id, f"{One_data[1]['Error']}")
                    return 1

                templates[f"{message.from_user.id}"][templates[f"{message.from_user.id}"]['Number']] = message.text
                templates[f"{message.from_user.id}"]['Number'] = str(int(templates[f"{message.from_user.id}"]['Number']) + 1)


            elif templates[f"{message.from_user.id}"]['Number'] == '8':

                if not '@' in str(message.text):
                    print(f'неверно')
                    bot.send_message(message.from_user.id, f"{One_data[1]['Error']}")
                    return 1

                templates[f"{message.from_user.id}"][templates[f"{message.from_user.id}"]['Number']] = message.text
                templates[f"{message.from_user.id}"]['Number'] = str(int(templates[f"{message.from_user.id}"]['Number']) + 1)

            else:

                templates[f"{message.from_user.id}"][templates[f"{message.from_user.id}"]['Number']] = message.text
                templates[f"{message.from_user.id}"]['Number'] = str(int(templates[f"{message.from_user.id}"]['Number']) + 1)

        vopros_vi(bot, message.from_user.id, templates[f'{message.from_user.id}']['Number'])
        with open("data/data.json", "w", encoding='utf-8') as file:
            json.dump(templates, file, indent=4, ensure_ascii=False)

    except Exception as e:
       print(e)




@bot.message_handler(content_types=['document'])
def load(message):

    file_name = message.document.file_name


    file_id_info = (bot.get_file(message.document.file_id))
    downloaded_file = bot.download_file(file_id_info.file_path)


    for i in range(1000000):
        if not os.path.exists(f'Output/{message.from_user.id}_{1}.{str(file_name).split(".")[1]}'):
            with open(f'Output/{message.from_user.id}_{1}.{str(file_name).split(".")[1]}', 'wb') as foto:
                foto.write(downloaded_file)
            break





def processPhotoMessage(message):

    fileID = message.photo[-1].file_id

    file = bot.get_file(fileID)


    file_save = requests.get(url = f'https://api.telegram.org/file/bot{token}/{file.file_path}', stream=True)

    for i in range(1000000):
        if not os.path.exists(f'Output/{message.from_user.id}_{i}.jpg'):

            with open(f'Output/{message.from_user.id}_{i}.jpg', 'wb') as foto:
                foto.write(file_save.content)
            break


@bot.message_handler(content_types=['photo'])
def photo(message):
    processPhotoMessage(message)



@bot.message_handler(content_types=['video_note'])
def Video(message):

    file_info = bot.get_file(message.video_note.file_id)

    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path), stream=True)

    for i in range(10000000):
        if not os.path.exists(f'Output/{message.from_user.id}_{i}.mp4'):
            with open(f'Output/{message.from_user.id}_{i}.mp4', 'wb') as foto:
                foto.write(file.content)
            break



def processVideoMessage(message):

    fileID = message.video.file_id

    file = bot.get_file(fileID)


    file_save = requests.get(url=f'https://api.telegram.org/file/bot{token}/{file.file_path}', stream=True)

    for i in range(10000000):
        if not os.path.exists(f'Output/{message.from_user.id}_{i}.mp4'):
            with open(f'Output/{message.from_user.id}_{i}.mp4', 'wb') as foto:
                foto.write(file_save.content)
            break




@bot.message_handler(content_types=['video'])
def video_save(message):
    processVideoMessage(message)


@bot.message_handler(content_types=['voice','text'])
def repeat_all_message(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path), stream=True)


    for i in range(10000000):
        if not os.path.exists(f'Output/{message.from_user.id}_{i}.ogg'):
            with open(f'Output/{message.from_user.id}_{i}.ogg', 'wb') as foto:
                foto.write(file.content)
            break


# bot.polling()
#

while True:
    try:
        print("[*] bot starting..")

        bot.polling(none_stop=True, interval=2)
        # Предполагаю, что бот может мирно завершить работу, поэтому
        # даем выйти из цикла
        break

    except Exception as ex:
        print("[*] error - {}".format(str(ex))) # Описание ошибки


        print("[*] rebooting..")
            # bot.send_message(int(admin), "[*] rebooting..")

        bot.stop_polling()
        # Останавливаем чтобы не получить блокировку
        time.sleep(15)
        print("[*] restarted!")

#
