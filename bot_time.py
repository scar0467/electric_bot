import telebot
import time
from datetime import datetime
from token1 import token_bot
#import schedule

bot = telebot.TeleBot( token_bot)
#BOT_URL = "URL"

# @bot.message_handler(commands=['start'])
# def start_message(message):
#     print(message)

# now = datetime.now()
# print(now)
# current_time = now.strftime("%H:%M")

# # def job():
# #    bot.send_message(4237474377, ' Привет')

# # schedule.every(10).seconds.do(job)
# # while True:
# #    schedule.run_pending()
# #    time.sleep(1)
ls=[1047877068 ,6402335526,6456585499]
#ls=[1047877068 'мой',6402335526 'тех.под',6456585499 'тест АЗС94']


#Запускаем цикл для проверки времени
while True:
    time.sleep(1)
    now = datetime.now()
    #print(now.strftime("%H:%M:%S"))
    current_time = now.strftime("%H:%M:%S")
    if current_time == '17:05:00':#Выставляете ваше время
       print('pass')
       for id in ls:
          bot.send_message(id, f'Текущее время: {current_time}')
    elif current_time == '18:08:00':
        for id in ls:
            bot.send_message(id, f'Текущее время: {current_time}')

    elif current_time == '19:06:00':
        for id in ls:
            bot.send_message(id, f'Текущее время: {current_time}')

    elif current_time == '20:44:00':
        for id in ls:
            bot.send_message(id, f'Текущее время: {current_time}')

#bot.infinity_polling()
