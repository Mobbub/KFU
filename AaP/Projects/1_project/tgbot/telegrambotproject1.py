import requests
import telebot
from telebot import types

bot = telebot.TeleBot('6952931811:AAGaxnDxuIeDmcfB460Ce6JVlvMXJ2En278')
flag1 = False
flag2 = False
flag3 = False
flag4 = False
flag5 = False
flag6 = False
flag7 = False
flag8 = False
flag9 = False
flag10 = False
flag11 = False
flag12 = False
fio = ''
dr = ''
ds = ''
mr = ''
ms = ''
supr = ''
obr = ''
rd = ''
graj = ''
deti = ''
vnuki = ''
dost = ''
deys = ''

def main(fio, dr, ds, mr, ms, supr, obr, rd, graj, deti, vnuki, dost, deys):
    pass

def prov(mes, vopr):
    pass

@bot.message_handler(commands = ['start'])
def start(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text = 'Эпитафия')
    btn2 = types.KeyboardButton(text = 'Биография')
    kb.add(btn1)
    kb.add(btn2)
    bot.send_message(message.chat.id, 'Здрасьте. Выберете действие', reply_markup=kb)

@bot.message_handler(func = lambda message: message.text == 'Эпитафия')
def epitafia(message):
    global flag1, deys
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text = 'Следующий вопрос')
    btn2 = types.KeyboardButton(text = 'Прошлый вопрос')
    btn3 = types.KeyboardButton(text = 'Начать заново')
    kb.add(btn2, btn3)
    kb.add(btn1)
    flag1 = True
    deys = 'Эпитафия'
    bot.send_message(message.chat.id, '''Введите ФИО.
Например: Иванов Иван Иванович''', reply_markup=kb)
    
@bot.message_handler(func = lambda message: message.text == 'Биография')
def biografia(message):
    global flag1, deys
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text = 'Следующий вопрос')
    btn2 = types.KeyboardButton(text = 'Прошлый вопрос')
    btn3 = types.KeyboardButton(text = 'Начать заново')
    kb.add(btn2, btn3)
    kb.add(btn1)
    flag1 = True
    deys = 'Биография'
    bot.send_message(message.chat.id, '''Введите ФИО.
Например: Иванов Иван Иванович''', reply_markup=kb)
    
@bot.message_handler(func = lambda message: message.text == f'Другой {deys}')
def noviy(message):
    global fio, dr, ds, mr, ms, supr, obr, rd, graj, deti, vnuki, dost, deys
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text = f'Другой {deys}')
    btn2 = types.KeyboardButton(text = 'Начать заново')
    kb.add(btn1)
    kb.add(btn2)
    bot.send_message(message.chat.id, '''Вот {deys}
{main(fio, dr, ds, mr, ms, supr, obr, rd, graj, deti, vnuki, dost, deys)}''', reply_markup=kb)
    
@bot.message_handler(func = lambda message: message.text == 'Начать заново')
def zanovo(message):
    global flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, flag9, flag10, flag11, flag12, fio, dr, ds, mr, ms, supr, obr, rd, graj, deti, vnuki, dost, deys
    flag1 = False
    flag2 = False
    flag3 = False
    flag4 = False
    flag5 = False
    flag6 = False
    flag7 = False
    flag8 = False
    flag9 = False
    flag10 = False
    flag11 = False
    flag12 = False
    fio = ''
    dr = ''
    ds = ''
    mr = ''
    ms = ''
    supr = ''
    obr = ''
    rd = ''
    graj = ''
    deti = ''
    vnuki = ''
    dost = ''
    deys = ''    
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text = 'Эпитафия')
    btn2 = types.KeyboardButton(text = 'Биография')
    kb.add(btn1)
    kb.add(btn2)
    bot.send_message(message.chat.id, 'Выберете действие', reply_markup=kb)

@bot.message_handler(func = lambda message: True)
def info(message):
    global flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, flag9, flag10, flag11, flag12, fio, dr, ds, mr, ms, supr, obr, rd, graj, deti, vnuki, dost, deys
    if flag1:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text = 'Следующий вопрос')
        btn2 = types.KeyboardButton(text = 'Прошлый вопрос')
        btn3 = types.KeyboardButton(text = 'Начать заново')
        kb.add(btn2, btn3)
        kb.add(btn1)
        if prov(message.text, 'ФИО'):
            fio = message.text
            flag2 = True
            message.text = ''
            flag1 = False
            bot.send_message(message.chat.id, '''Введите дату рождения. 
Например: 01.01.2000''', reply_markup=kb)
        else:
            bot.send_message(message.chat.id, '''Что то пошло не так, введите ФИО ещё раз, проверьте правильность написания. 
Например: ''', reply_markup=kb)
    elif flag2:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text = 'Следующий вопрос')
        btn2 = types.KeyboardButton(text = 'Прошлый вопрос')
        btn3 = types.KeyboardButton(text = 'Начать заново')
        kb.add(btn1, btn2)
        kb.add(btn3)
        if prov(message.text, 'ДР'):
            dr = message.text
            flag3 = True
            message.text = ''
            flag2 = False
            bot.send_message(message.chat.id, '''Введите дату смерти. 
Например: 01.01.2000''', reply_markup=kb)
        else:
            bot.send_message(message.chat.id, '''Что то пошло не так, введите дату рождения ещё раз, проверьте правильность написания. 
Например: 01.01.2000''', reply_markup=kb)
    elif flag3:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text = 'Следующий вопрос')
        btn2 = types.KeyboardButton(text = 'Прошлый вопрос')
        btn3 = types.KeyboardButton(text = 'Начать заново')
        kb.add(btn1, btn2)
        kb.add(btn3)
        if prov(message.text, 'ДС'):
            ds = message.text
            flag4 = True
            message.text = ''
            flag3 = False
            bot.send_message(message.chat.id, '''Введите место рождения. 
Например: Россия''', reply_markup=kb)
        else:
            bot.send_message(message.chat.id, '''Что то пошло не так, введите дату смерти ещё раз, проверьте правильность написания. 
Например: 01.01.2000''', reply_markup=kb)
    elif flag4:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text = 'Следующий вопрос')
        btn2 = types.KeyboardButton(text = 'Прошлый вопрос')
        btn3 = types.KeyboardButton(text = 'Начать заново')
        kb.add(btn1, btn2)
        kb.add(btn3)
        if prov(message.text, 'МР'):
            mr = message.text
            flag5 = True
            message.text = ''
            flag4 = False
            bot.send_message(message.chat.id, '''Введите место смерти.
Например: Россия''', reply_markup=kb)
        else:
            bot.send_message(message.chat.id, '''Что то пошло не так, введите место рождения ещё раз, проверьте правильность написания. 
Например: Россия''', reply_markup=kb)
    elif flag5:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text = 'Следующий вопрос')
        btn2 = types.KeyboardButton(text = 'Прошлый вопрос')
        btn3 = types.KeyboardButton(text = 'Начать заново')
        kb.add(btn1, btn2)
        kb.add(btn3)
        if prov(message.text, 'МС'):
            ms = message.text
            flag6 = True
            message.text = ''
            flag5 = False
            bot.send_message(message.chat.id, '''Введите ФИО супруга(ги).
Например: Иванов Иван Иванович''', reply_markup=kb)
        else:
            bot.send_message(message.chat.id, '''Что то пошло не так, введите место смерти ещё раз, проверьте правильность написания. 
Например: Россия''', reply_markup=kb)
    elif flag6:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text = 'Следующий вопрос')
        btn2 = types.KeyboardButton(text = 'Прошлый вопрос')
        btn3 = types.KeyboardButton(text = 'Начать заново')
        kb.add(btn1, btn2)
        kb.add(btn3)
        if prov(message.text, 'Супруг'):
            supr = message.text
            flag7 = True
            message.text = ''
            flag6 = False
            bot.send_message(message.chat.id, '''Укажите учебное заведение, которое закончил этот человек.
Например: Физико-технический институ (ФТИ) КФУ им. Вернадского''', reply_markup=kb)
        else:
            bot.send_message(message.chat.id, '''Что то пошло не так, введите ФИО супруга(ги) ещё раз, проверьте правильность написания. 
Например: Иванов Иван Иванович''', reply_markup=kb)
    elif flag7:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text = 'Следующий вопрос')
        btn2 = types.KeyboardButton(text = 'Прошлый вопрос')
        btn3 = types.KeyboardButton(text = 'Начать заново')
        kb.add(btn1, btn2)
        kb.add(btn3)
        if prov(message.text, 'обр'):
            obr = message.text
            flag8 = True
            message.text = ''
            flag7 = False
            bot.send_message(message.chat.id, '''Укажите род деятельности человека.
Например: Учёный математик''', reply_markup=kb)
        else:
            bot.send_message(message.chat.id, '''Что то пошло не так, введите учебное заведение, которое закончил этот человек, проверьте правильность написания. 
Например: Физико-технический институ (ФТИ) КФУ им. Вернадского''', reply_markup=kb)
    elif flag8:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text = 'Следующий вопрос')
        btn2 = types.KeyboardButton(text = 'Прошлый вопрос')
        btn3 = types.KeyboardButton(text = 'Начать заново')
        kb.add(btn1, btn2)
        kb.add(btn3)
        if prov(message.text, 'РД'):
            rd = message.text
            flag9 = True
            message.text = ''
            flag8 = False
            bot.send_message(message.chat.id, '''Укажите гражданство человека.
Например: Россия''', reply_markup=kb)
        else:
            bot.send_message(message.chat.id, '''Что то пошло не так, введите род деятельности человека, проверьте правильность написания. 
Например: Учёный математик''', reply_markup=kb)
    elif flag9:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text = 'Следующий вопрос')
        btn2 = types.KeyboardButton(text = 'Прошлый вопрос')
        btn3 = types.KeyboardButton(text = 'Начать заново')
        kb.add(btn1, btn2)
        kb.add(btn3)
        if prov(message.text, 'ГРАЖ'):
            graj = message.text
            flag10 = True
            message.text = ''
            flag9 = False
            bot.send_message(message.chat.id, '''Укажите ФИО детей.
Например: Иванов Иван Иванович''', reply_markup=kb)
        else:
            bot.send_message(message.chat.id, '''Что то пошло не так, введите гражданство человека, проверьте правильность написания. 
Например: Россия''', reply_markup=kb)
    elif flag10:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text = 'Следующий вопрос')
        btn2 = types.KeyboardButton(text = 'Прошлый вопрос')
        btn3 = types.KeyboardButton(text = 'Начать заново')
        kb.add(btn1, btn2)
        kb.add(btn3)
        if prov(message.text, 'Дети'):
            deti = message.text
            flag11 = True
            message.text = ''
            flag10 = False
            bot.send_message(message.chat.id, '''Укажите ФИО внуков:
Например: Иванов Иван Иванович''', reply_markup=kb)
        else:
            bot.send_message(message.chat.id, '''Что то пошло не так, введите ФИО детей, проверьте правильность написания. 
Например: Иванов Иван Иванович''', reply_markup=kb)
    elif flag11:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text = 'Следующий вопрос')
        btn2 = types.KeyboardButton(text = 'Прошлый вопрос')
        btn3 = types.KeyboardButton(text = 'Начать заново')
        kb.add(btn1, btn2)
        kb.add(btn3)
        if prov(message.text, 'Внуки'):
            vnuki = message.text
            flag12 = True
            message.text = ''
            flag11 = False
            bot.send_message(message.chat.id, '''Введите награды, премии или достижения, которые есть у человека.
Например: Знак Почета 1954, 1981''', reply_markup=kb)
        else:
            bot.send_message(message.chat.id, '''Что то пошло не так, введите ФИО внуков, проверьте правильность написания. 
Например: Иванов Иван Иванович''', reply_markup=kb)
    elif flag12:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text = f'Другой {deys}')
        btn2 = types.KeyboardButton(text = 'Начать заново')
        kb.add(btn1)
        kb.add(btn2)
        if prov(message.text, 'дост'):
            dost = message.text
            flag12 = False
            bot.send_message(message.chat.id, f'''Вот {deys}:
{main(fio, dr, ds, mr, ms, supr, obr, rd, graj, deti, vnuki, dost, deys)}''', reply_markup=kb)
        else:
            bot.send_message(message.chat.id, '''Что то пошло не так, введите награды, премии или достижения, которые есть у человека, проверьте правильность написания. 
Например: Знак Почета 1954, 1981''', reply_markup=kb)
    else:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text = 'Эпитафия')
        btn2 = types.KeyboardButton(text = 'Биография')
        kb.add(btn1)
        kb.add(btn2)
        bot.send_message(message.chat.id, 'моя твоя не понимать')
        bot.send_message(message.chat.id, 'Выберете действие', reply_markup=kb)

bot.polling()
