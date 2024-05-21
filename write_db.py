from conn import connection
#import pandas as pd
import re
import sqlite3
import  time
import locale
#from bs4 import BeautifulSoup
#from bot import inf_to_bot


locale.setlocale(locale.LC_ALL, 'Russian_Russia.1251')


#cursor=connect.cursor()

def num_azs(name_user):
    return re.findall(r'[-+]?\d+',name_user)[0]




def write(name_user,id_user,pokazaniya,df_dog,date_otch,date_time_otch):
    print((re.findall(r'[-+]?\d+',name_user))[0],id_user,pokazaniya)
    print(df_dog.info())
    df_dog=df_dog.drop_duplicates(['Объект'], keep='last')
    df_dog=df_dog[df_dog['Инд_телеграм'].isin([str(id_user)])]
    print(df_dog)
    print(df_dog.iloc[0])
    #print(df_dog.loc['Объект'])
    relevant_table=f"{df_dog.iloc[0]['Номер_договора']}_{df_dog.iloc[0]['Объект']}"



    connection
    cursor=connection.cursor()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS '{relevant_table}' (
                    Показание TEXT ,
                    Расход_за_сутки,
                    Дата  timestamp UNIQUE,
                    Дата_время timestamp,
                    Плательщик TEXT NOT NULL,
                    Способ TEXT NOT NULL

                    )
                    ''')

    cursor.execute(f"SELECT Дата, Показание, Расход_за_сутки, Дата_время  FROM '{relevant_table}' ORDER BY `Дата` DESC LIMIT 30")
    available_tables= cursor.fetchall()
    print(available_tables)


    _sum = 0
    for i in available_tables:
        _sum += int(i[2])
    median = _sum//len(available_tables)


    # date_otch=time.strftime('%x')
    # date_time_otch=time.strftime('%c')

    r=0
    try:
        print(available_tables[0][0])
        if date_otch != available_tables[0][0]:
            sutochn=int(pokazaniya) - int(available_tables[0][1])
            delta = int(pokazaniya) - int(available_tables[0][1]) - int(available_tables[0][2])
            print(delta)

            # if delta < 1:
            #     text=f"""<b>Проверьте правильность введённых данных</b>\nРасход электроэнергии не должен быть меньше или ровняться нулю.
            # """
            #     return te
            if sutochn < 1:
                text=f"""<b>Проверьте правильность введённых данных</b>\nРасход электроэнергии не должен быть меньше или ровняться нулю.
            """
                return text
            elif sutochn > median * 2:
                text = "подтверждение"
            #     text=f"""<b>Проверьте правильность введённых данных</b>\nРасход электроэнергии за смену превышает среднестатистический, более чем в {int(sutochn/median)} раза.
            # """
                return text, sutochn, median


            print(date_otch,available_tables[0][0])
            cursor.execute(f'INSERT INTO `{relevant_table}` (Показание,Расход_за_сутки, Дата, Дата_время, Плательщик, Способ) VALUES (?, ?, ?, ?, ?,?)', (int(pokazaniya), sutochn,date_otch, date_time_otch,df_dog.iloc[0]['Плательщик'], df_dog.iloc[0]['Способ']))
            connection.commit()
            try:
                procent=round(((sutochn-int(available_tables[0][2]))/int(available_tables[0][2]))*100, 1)


            except ZeroDivisionError:
                text="""В дальнешем, когда у меня будет больше информации, в ответ на Ваше сообщение я буду отправлять Вам информацию о количестве кВт израсходованных за смену и
инфрмацию о том, на сколько больше или меньше было израсходовано электроэнергии в сравнение с предыдущей сменой.\n"""
                return text
            if sutochn <= int(available_tables[0][2]):
                text=f"""<b>Информация по расходу эл.энергии</b>
            Израсходовано э/э за смену - <b>{sutochn} кВт/ч</b>
            что на <b>{procent-procent*2}%</b> меньше чем расход  за предыдущую смену."""
                return text

            elif sutochn > int(available_tables[0][2]):
                text=(f"""<b>Информация по расходу эл.энергии</b>
            Израсходовано э/э за смену - <b>{sutochn} кВт/ч,</b>
            что на <b>{procent}%</b> больше чем расход  за предыдущую смену.""")

                return text


        elif date_otch == available_tables[0][0]:
            text=f'Показание за эту дату передавались {available_tables[0][0]}'
            return text

    except IndexError:
        cursor.execute(f'INSERT INTO `{relevant_table}` (Показание,Расход_за_сутки, Дата, Дата_время, Плательщик, Способ) VALUES (?, ?, ?, ?, ?,?)', (pokazaniya, '0',date_otch, date_time_otch,df_dog.iloc[0]['Плательщик'], df_dog.iloc[0]['Способ']))
        connection.commit()


    except sqlite3.IntegrityError:
        pass
