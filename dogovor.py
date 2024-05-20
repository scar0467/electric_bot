from  conn import connection
import sqlite3


dogovor=input('Договор:')
azs = input('Номер АЗС:')
object_=input('Объект:')
platelschik=input('Плательщик:')
sposob=input('Способ передачи:')

while dogovor !='':
    connection
    cursor=connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Договор (
    Номер_договора PRIMARY KEY,
    Номер_АЗС TEXT TEXT NOT NULL,
    Объект TEXT NOT NULL,
    Плательщик TEXT NOT NULL,
    Способ TEXT NOT NULL
    )
    ''')

    connection.commit()




    try:

        cursor.execute('INSERT INTO Договор (Номер_договора,Номер_АЗС,Объект, Плательщик, Способ ) VALUES (?, ?, ?, ?, ?)', (dogovor,azs,object_,platelschik,sposob))

        connection.commit()

    except sqlite3.IntegrityError:
        print("Номер договора уже есть в базе")







    dogovor=input('Договор:')
    azs = input('Номер АЗС:')
    object_=input('Объект:')
    platelschik=input('Плательщик:')
    sposob=input('Способ передачи:')

connection.commit()
connection.close()
