import telebot
import pandas as pd
from telebot import types
from write_db import write,num_azs, write_1
from conn import connection
import time
import datetime
import locale
from token1 import token_bot, id_support
import schedule
import threading

locale.setlocale(locale.LC_ALL, 'Russian_Russia.1251')


bot = telebot.TeleBot(token_bot)

def start_polling():
    bot.infinity_polling(none_stop=True)

polling_thread = threading.Thread(target=start_polling)
polling_thread.start()


@bot.message_handler(commands=['start'])
def start_message(message):
    global ls_id
    try:
        connection
        cursor=connection.cursor()
        cursor.execute(f"""UPDATE Договор
                    SET Инд_телеграм = {message.chat.id}
                    WHERE Номер_АЗС = '{num_azs(message.from_user.first_name)}' AND Инд_телеграм = '';""")
        connection.commit()
        cursor.close
        df_dog = pd.read_sql_query("SELECT Номер_договора,Номер_АЗС, Объект, Плательщик, Способ, Инд_телеграм  FROM Договор", connection)
        ls_id = [value for value in df_dog['Инд_телеграм'].to_list() if value]
        if str(message.from_user.id) in ls_id:
            bot.send_message(message.chat.id,f'<b>{message.from_user.first_name}</b>, здравствуйте! Авторизация прошла успешно. Можете передать показания\n',parse_mode='html')
            bot.send_message(id_support, f'<b>{message.from_user.first_name}</b>, авторизовался',parse_mode='html')
        else:
            bot.send_message(message.chat.id,f'<b>{message.from_user.first_name}</b>, здравствуйте! Ваш аккаунт не авторизован. Вход запрещён\n',parse_mode='html')
    except IndexError: #sqlite3.OperationalError:
        bot.send_message(message.chat.id,f'<b>{message.from_user.first_name}</b>, здравствуйте! Авторизация запрещена.\n',parse_mode='html')


@bot.message_handler(content_types=["text"])
def handle_text(message):
    #print(message)
    global text

    if datetime.date.fromtimestamp(message.date) < datetime.date(2024,5,22):
        bot.send_message(message.chat.id,f'<b>{message.from_user.first_name}</b>, показание приборов можно будет отправлять с 25.05.2024\n',parse_mode='html')
    else:
        legal_date(message)


def legal_date(message):
    global name_user,id_user,pokazaniya,date_otch,date_time_otch
    df_dog = pd.read_sql_query("SELECT Номер_договора,Номер_АЗС, Объект, Плательщик, Способ, Инд_телеграм  FROM Договор", connection)
    ls_id = df_dog['Инд_телеграм'].to_list()
    try:
        if str(message.from_user.id) in ls_id:
            name_user = message.from_user.first_name
            id_user = message.from_user.id
            pokazaniya = round(float(message.text.replace(',','.')),1)
            date_otch=time.strftime('%Y.%m.%d',time.localtime(message.date))
            date_time_otch=time.strftime('%d.%m.%Y %H:%M:%S',time.localtime(message.date))
            text=write(name_user,id_user,pokazaniya,df_dog,date_otch,date_time_otch)
            if text[0]=='подтверждение':
                message_button(message,text)
            elif text=='0':
                bot.send_message(message.chat.id,f"""<b>{message.from_user.first_name}</b>, показания прибора учёта приняты.
        В дальнейшем, когда у меня будет больше информации, в ответ на ваше сообщение я буду отправлять вам информацию о количестве кВт израсходованных за смену и
        инфрмацию о том, на сколько больше или меньше было израсходовано электроэнергии по сравнению с предыдущей сменой.\n""",parse_mode='html')
            else:
                bot.send_message(message.chat.id,text,parse_mode='html')
        else:
            bot.send_message(message.chat.id,f'<b>{message.from_user.first_name}</b>, Вы не авторизованы. Вы не можете отправлять сообщения боту\n',parse_mode='html')
    except ValueError:
        bot.send_message(message.chat.id,f'<b>Введённые показания не должны содержать буквы и символы. Только цифры.</b>\n',parse_mode='html')

def message_button(message,text):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Всё равно продолжить", callback_data="test")
    keyboard.add(callback_button)
    try:
       bot.send_message(message.chat.id,f'<b>Проверьте правильность введённых данных</b>\nРасход электроэнергии за смену превышает среднестатистический, более чем в {int(text[1]/text[2])} раза.\n',parse_mode='html',reply_markup=keyboard)
    except ZeroDivisionError:
        bot.send_message(message.chat.id,f'<b>Показания приняты</b>',parse_mode='html')
        write_1()

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        text=write_1()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text,parse_mode='html')

    except telebot.apihelper.ApiTelegramException:
        pass

def send_message():
    df_dog = pd.read_sql_query("SELECT Номер_договора,Номер_АЗС, Объект, Плательщик, Способ, Инд_телеграм  FROM Договор", connection)
    ls_id = [value for value in df_dog['Инд_телеграм'].to_list() if value]
    for i in ls_id:
        bot.send_message(i, 'Не забудьте до 09:00 передать показания приборов учёта электроэнергии')

def no_data():
    tables = pd.read_sql_query("SELECT * FROM sqlite_master WHERE type='table';", connection)
    ls_no_data=()
    connection
    cursor=connection.cursor()
    for table in tables['tbl_name'][1::]:
        print(table)
        cursor.execute(f"SELECT Дата FROM '{table}'WHERE Дата == '{time.strftime('%Y.%m.%d',time.localtime())}' ORDER BY `Дата` DESC LIMIT 1")
        data= cursor.fetchall()
        if data == []:
            ls_no_data += (table,)
        try:
           bot.send_message(id_support, ls_no_data)
           ls_no_data=()
        except:
            bot.send_message(id_support, "Все передали")
    cursor.close


if __name__ == '__main__':
    def start_polling():
        bot.infinity_polling(none_stop=True)

        polling_thread = threading.Thread(target=start_polling)
        polling_thread.start()
    schedule.every().day.at("08:00").do(send_message)
    schedule.every().day.at("09:15").do(no_data)
    #schedule.every().day.at("10:25").do(no_data)

    while True:
        schedule.run_pending()
        time.sleep(1)
