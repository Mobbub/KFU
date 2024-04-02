import requests
from flask import Flask
from flask import request
import telebot #подключение библиотеки
from telebot import types #подключаем кнопки (types) из библиотеки
import _thread
import http.server
import json
import re

bot = telebot.TeleBot('6577398836:AAGolYrHqOtnXaaiOctxqBGc3YL4B9OCaG4') #токен бота
chat_idishnik = 0
flag1 = False
flag2 = False
flag3 = False
flag4 = False
flag5 = False
flag6 = False
flag7 = False
flag8 = False
name = ''
surname = ''
surname_next = ''
zapr_deyst = ''
idgit = ''

def serv():
    class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            json_data = json.loads(post_data)
            print(json_data)
            reg(json_data)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Success')

    if __name__ == '__main__':
        server_address = ('', 8000)
        httpd = http.server.HTTPServer(server_address, MyHTTPRequestHandler)
        httpd.serve_forever()

_thread.start_new_thread(serv, ())

def reg(otv): ###
    idgit = otv.get('IDgit', 'None')
    chatid = otv.get('ChatID', 'None')
    if idgit == '\x00':
        bot.send_message(int(chatid), 'Вы не зарегистрировались')
    else:
        with open('ses.txt', 'a') as file:
            file.write(f'{chatid} {idgit}\n')
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text = 'Где следующая пара')
            btn2 = types.KeyboardButton(text = 'Расписание на [день недели]')
            btn3 = types.KeyboardButton(text = 'Расписание на сегодня')
            btn4 = types.KeyboardButton(text = 'Расписание на завтра')
            btn5 = types.KeyboardButton(text = 'Оставить комментарий к [номер] паре [для группы]')
            btn6 = types.KeyboardButton(text = 'Где группа/подгруппа')
            btn7 = types.KeyboardButton(text = 'Где преподаватель')
            btn8 = types.KeyboardButton(text = 'Когда экзамен')
            kb.add(btn1, btn2)
            kb.add(btn3, btn4)
            kb.add(btn5, btn6)
            kb.add(btn7, btn8)
            bot.send_message(int(chatid), 'Вы успешно авторизовались! Выберете действие', reply_markup=kb)

def proversession(chat_idishnik): ###
    with open('ses.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if str(chat_idishnik) in line:
                return True
            return False

def zapravtorise_avt(chat_idishnik, surname, name, surname_next):
    global response
    url = 'http://192.168.253.179:8080/Authorization'
    parameters = {
        'ChatID': str(chat_idishnik),
        'Surname': surname,
        'Name': name,
        'Surname_next': surname_next
    }
    response = requests.post(url, params=parameters)
    print(response.content)
    return response.content

def zapr_avt(zapr_deyst, chat_idishnik):
    with open('input.txt', 'r') as f_in, open('output.txt', 'w') as f_out:
        for line in f_in:
            match = re.search(r'00004444 (\d+)', line)
            if match:
                pass
    global response
    url = 'http://192.168.253.179:8080/Surgery'
    parameters = {
        'IDgit': 1,
        'Request': zapr_deyst
    }
    response = requests.post(url, params=parameters)    
    return response.content

def zaprasp_serv(jwt):
    global response
    url = 'http://26.237.88.118:8060/tgbot' ###
    parameters = jwt
    response = requests.post(url, params=parameters)
    return response.content

def h(chat_id):
    pass

@bot.message_handler(commands = ['start']) 
def start(message): 
    global chat_idishnik, flag6, name, surname, surname_next
    chat_idishnik = message.chat.id
    if proversession(chat_idishnik):
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text = 'Где следующая пара')
        btn2 = types.KeyboardButton(text = 'Расписание на [день недели]')
        btn3 = types.KeyboardButton(text = 'Расписание на сегодня')
        btn4 = types.KeyboardButton(text = 'Расписание на завтра')
        btn5 = types.KeyboardButton(text = 'Оставить комментарий к [номер] паре [для группы]')
        btn6 = types.KeyboardButton(text = 'Где группа/подгруппа')
        btn7 = types.KeyboardButton(text = 'Где преподаватель')
        btn8 = types.KeyboardButton(text = 'Когда экзамен')
        btn9 = types.KeyboardButton(text = 'Администрирование')
        kb.add(btn1, btn2)
        kb.add(btn3, btn4)
        kb.add(btn5, btn6)
        kb.add(btn7, btn8)
        kb.add(btn9)
        bot.send_message(message.chat.id, 'Выберете действие', reply_markup=kb) #команда, которая выводит текст на команду /start
    else:
        name = ''
        surname = ''
        surname_next = ''
        flag6 = True
        bot.send_message(message.chat.id, 'Для авторизации введите своё ФИО')
        #bot.send_message(message.chat.id, f'''Войдите в нашу систему {zapravtorise_avt(chat_idishnik)}''')

@bot.message_handler(func = lambda message: message.text == 'Администрирование')
def gde_para(message):
    global chat_idishnik, flag6
    chat_idishnik = message.chat.id
    if proversession(chat_idishnik):
        bot.send_message(message.chat.id, 'http://26.70.121.176:8085/')
    else:
        bot.send_message(message.chat.id, 'Для авторизации введите вашу фамилию')
        flag6 = True

@bot.message_handler(fanc=lambda message: message.text == 'Где следующая пара')
def gde_para(message):
    global chat_idishnik, zapr_deyst, flag6
    chat_idishnik = message.chat.id
    if proversession(chat_idishnik):
        zapr_deyst = ''    
        zapr_deyst += 'Где следующая пара' 
        bot.send_message(message.chat.id, zaprasp_serv(zapr_avt(idgit, zapr_deyst)))
        zapr_deyst = ''
    else:
        bot.send_message(message.chat.id, 'Для авторизации введите вашу фамилию')
        flag6 = True

@bot.message_handler(fanc=lambda message: message.text == 'Расписание на [день недели]') 
def rasp_den(message):
    global chat_idishnik, zapr_deyst, flag1, flag6
    chat_idishnik = message.chat.id
    if proversession(chat_idishnik):
        zapr_deyst = ''
        flag1 = True
        zapr_deyst += 'Расписание на '
        bot.send_message(message.chat.id, 'Введите полное название дня недели')
    else:
        bot.send_message(message.chat.id, 'Для авторизации введите вашу фамилию')
        flag6 = True

@bot.message_handler(fanc=lambda message: message.text == 'Расписание на сегодня') 
def rasp_segod(message):
    global chat_idishnik, zapr_deyst, flag6
    chat_idishnik = message.chat.id
    if proversession(chat_idishnik):
        zapr_deyst = ''     
        zapr_deyst += 'Расписание на сегодня'
        bot.send_message(message.chat.id, zaprasp_serv(zapr_avt(idgit, zapr_deyst)))
        zapr_deyst = ''
    else:
        bot.send_message(message.chat.id, 'Для авторизации введите вашу фамилию')
        flag6 = True

@bot.message_handler(fanc=lambda message: message.text == 'Расписание на завтра') 
def rasp_zavt(message):
    global chat_idishnik, zapr_deyst, flag6
    chat_idishnik = message.chat.id
    if proversession(chat_idishnik):
        zapr_deyst = '' 
        zapr_deyst += 'Расписание на завтра'
        bot.send_message(message.chat.id, zaprasp_serv(zapr_avt(idgit, zapr_deyst)))
        zapr_deyst = ''
    else:
        flag6 = True
        bot.send_message(message.chat.id, 'Для авторизации введите вашу фамилию')

@bot.message_handler(func=lambda message: message.text == 'Оставить комментарий к [номер] паре [для группы]') ### 
def ost_com(message):
    global chat_idishnik, zapr_deyst, flag5, flag6
    if proversession(chat_idishnik):
        chat_idishnik = message.chat.id
        zapr_deyst = ''
        zapr_deyst += 'Оставить комментарий к '
        flag5 = True
        bot.send_message(message.chat.id, 'Введите номер пары и название группы слитно в одном сообщении')
    else:
        bot.send_message(message.chat.id, 'Для авторизации введите вашу фамилию')
        flag6 = True

@bot.message_handler(func=lambda message: message.text == 'Где группа/подгруппа')
def gde_grupa(message):
    global chat_idishnik, zapr_deyst, flag2, flag6
    if proversession(chat_idishnik):
        chat_idishnik = message.chat.id
        zapr_deyst = ''
        zapr_deyst += 'Где '
        flag2 = True
        bot.send_message(message.chat.id, 'Введите полное название группы')
    else:
        bot.send_message(message.chat.id, 'Для авторизации введите вашу фамилию')
        flag6 = True

@bot.message_handler(func=lambda message: message.text == 'Где преподаватель') 
def gde_prep(message):
    global chat_idishnik, zapr_deyst, flag3, flag6
    chat_idishnik = message.chat.id
    if proversession(chat_idishnik):
        zapr_deyst = '' 
        zapr_deyst += 'Где преподаватель'
        flag3=True
        bot.send_message(message.chat.id, 'Введите фамилию преподавателя')
    else:
        bot.send_message(message.chat.id, 'Для авторизации введите вашу фамилию')
        flag6 = True

@bot.message_handler(func=lambda message: message.text == 'Когда экзамен') ###
def kogda_exz(message):
    global chat_idishnik, zapr_deyst, flag4, flag6
    chat_idishnik = message.chat.id
    if proversession(chat_idishnik):
        zapr_deyst = '' 
        zapr_deyst += 'Где преподаватель'
        flag4=True
        bot.send_message(message.chat.id, 'Введите полное название предмета')
    else:
        bot.send_message(message.chat.id, 'Для авторизации введите вашу фамилию')
        flag6 = True

@bot.message_handler(func=lambda message: True)
def other(message):
    global name, surname, surname_next, zapr_deyst, idgit, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8
    a = message.text
    if flag1:
        zapr_deyst += a
        bot.send_message(message.chat.id, zaprasp_serv(zapr_avt(idgit, zapr_deyst)))
        zapr_deyst = ''
        flag1 = False
    if flag2:
        zapr_deyst += message.text
        bot.send_message(message.chat.id, zaprasp_serv(zapr_avt(idgit, zapr_deyst)))
        zapr_deyst = ''
        flag2 = False
    if flag3:
        zapr_deyst += message.text
        bot.send_message(message.chat.id, zaprasp_serv(zapr_avt(idgit, zapr_deyst)))
        zapr_deyst = ''
        flag3 = False
    if flag4:
        zapr_deyst += message.text
        bot.send_message(message.chat.id, zaprasp_serv(zapr_avt(idgit, zapr_deyst)))
        zapr_deyst = ''
        flag4 = False
    if flag5:
        zapr_deyst += message.text
        bot.send_message(message.chat.id, zaprasp_serv(zapr_avt(idgit, zapr_deyst)))
        zapr_deyst = ''
        flag5 = False
    if flag6:
        fio = message.text
        split_fio = fio.split()
        if len(split_fio) == 3:
            surname = split_fio[0]
            name = split_fio[1]
            patronymic = split_fio[2]
            bot.send_message(message.chat.id, f'''Войдите в нашу систему {zapravtorise_avt(chat_idishnik, surname, name, patronymic)}''')  

bot.polling()
