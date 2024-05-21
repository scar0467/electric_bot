import telebot
import os
import re
#import script
#import requests
import pandas as pd
from telebot import types
from write_db import write,num_azs
from conn import connection
import sqlite3
import time
import datetime
import locale
from token1 import token_bot

locale.setlocale(locale.LC_ALL, 'Russian_Russia.1251')



df_dog = pd.read_sql_query("SELECT Номер_договора,Номер_АЗС, Объект, Плательщик, Способ, Инд_телеграм  FROM Договор", connection)
ls_id = df_dog['Инд_телеграм'].to_list()
print(ls_id)


bot = telebot.TeleBot(token_bot)


@bot.message_handler(commands=['start'])
def start_message(message):
    print(num_azs(message.from_user.first_name))
    try:
        connection
        cursor=connection.cursor()
        cursor.execute(f"""UPDATE Договор
                    SET Инд_телеграм = {message.chat.id}
                    WHERE Номер_АЗС = {num_azs(message.from_user.first_name)} AND Инд_телеграм = '';""")
        connection.commit()
        df_dog = pd.read_sql_query("SELECT Номер_договора,Номер_АЗС, Объект, Плательщик, Способ, Инд_телеграм  FROM Договор", connection)
        ls_id = df_dog['Инд_телеграм'].to_list()
        print(ls_id)
        if str(message.from_user.id) in ls_id:
            bot.send_message(message.chat.id,f'<b>{message.from_user.first_name}</b>, здравствуйте! Авторизация прошла успешно.\n',parse_mode='html')
        else:
            bot.send_message(message.chat.id,f'<b>{message.from_user.first_name}</b>, здравствуйте! Ваш аккаунт не авторизован. Вход запрещён\n',parse_mode='html')
    except IndexError: #sqlite3.OperationalError:
        bot.send_message(message.chat.id,f'<b>{message.from_user.first_name}</b>, здравствуйте! Авторизация запрещена. <i>%%%ОШИБКА#<b>1</b>%%%%</i>\n',parse_mode='html')

    # df_dog = pd.read_sql_query("SELECT Номер_договора,Номер_АЗС, Объект, Плательщик, Способ, Инд_телеграм  FROM Договор", connection)
    # ls_id = df_dog['Инд_телеграм'].to_list()
    # print(ls_id)

    # if str(message.from_user.id) in ls_id:
    #         bot.send_message(message.chat.id,f'<b>{message.from_user.first_name}</b>, здравствуйте! Авторизация прошла успешно. Можете отправлять показания счётчика\n',parse_mode='html')
    #         bot.register_next_step_handler(message,handle_text)
    # else:
    #     bot.send_message(message.chat.id,f'<b>{message.from_user.first_name}</b>, здравствуйте! Ваш аккаунт не авторизован. Вход запрещён\n',parse_mode='html')



@bot.message_handler(content_types=["text"])
def handle_text(message):
    global text


    if datetime.date.fromtimestamp(message.date) < datetime.date(2024,5,21):
        bot.send_message(message.chat.id,f'<b>{message.from_user.first_name}</b>, показание приборов можно будет отправлять с 01.07.2024\n',parse_mode='html')


    else:
        legal_date(message)

def legal_date(message):
    df_dog = pd.read_sql_query("SELECT Номер_договора,Номер_АЗС, Объект, Плательщик, Способ, Инд_телеграм  FROM Договор", connection)
    ls_id = df_dog['Инд_телеграм'].to_list()
    #bot.send_message(message.chat.id,f'<b>{message.from_user.first_name}</b>, здравствуйте! Авторизация прошла успешно. Можете отправлять показания счётчика\n',parse_mode='html')
    if str(message.from_user.id) in ls_id:
        name_user = message.from_user.first_name
        id_user = message.from_user.id
        pokazaniya = round(float(message.text.replace(',','.')),1)
        date_otch=time.strftime('%d.%m.%Y',time.localtime(message.date))
        date_time_otch=time.strftime('%d.%m.%Y %H:%M:%S',time.localtime(message.date))

        print(name_user,id_user,pokazaniya,date_otch,date_time_otch)
        text=write(name_user,id_user,pokazaniya,df_dog,date_otch,date_time_otch)
        print(text)
        if text[0]=="подтверждение":
            message_button(message,text)
        else:
            try:
                bot.send_message(message.chat.id,text,parse_mode='html')

            except telebot.apihelper.ApiTelegramException:

                bot.send_message(message.chat.id,f"""<b>{message.from_user.first_name}</b>,
    в дальнешем, когда у меня будет больше информации, в ответ на Ваше сообщение я буду отправлять Вам информацию о количестве кВт израсходованных за смену и
    инфрмацию о том, на сколько больше или меньше было израсходовано электроэнергии в сравнение с предыдущей сменой.\n""",parse_mode='html')

        #write(name_user,id_user,pokazaniya,df_dog)
        #inf_to_bot(write(name_user,id_user,pokazaniya,df_dog))
        #bot.register_next_step_handler(message,second_message)


    #bot.send_message(message.chat.id,message)
    else:
        bot.send_message(message.chat.id,f'<b>{message.from_user.first_name}</b>, Вы не авторизованы. Вы не можете отправлять сообщения боту\n',parse_mode='html')

    #bot.send_message(message.chat.id, (message.text, message.from_user.first_name))
    #bot.send_message(message.chat.id, getwiki(message.text))
def message_button(message,text):
    bot.send_message(message.chat.id,f'<b>Проверьте правильность введённых данных</b>\nРасход электроэнергии за смену превышает среднестатистический, более чем в {int(text[1]/text[2])} раза.\n',parse_mode='html')
#print(date_time_otch)

#@bot.message_handler(func=lambda message: True)
# def inf_to_bot(r):
#     global text
#     text=r

#print(r)

# @bot.message_handler(content_types=["text"])
# def second_message(message):
#     print(22)

#     bot.send_message(message.chat.id,text)



bot.infinity_polling()
