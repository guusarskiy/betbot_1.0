import telebot
from telebot import types
import psycopg2
import webbrowser
import math

# host = 'localhost'
# dbname = 'betbot'
# user = 'postgres'
# password = 'TxpFH44T'
# host id = 5432

kosarID = 828453865
lemenkoID = 957793049
sozikID = 580699044
currentID = None
currentName = None

nameSql = None
passSql = None
betSql = None
betQuantity = None
outcome1 = None
outcome2 = None

botArg = telebot.TeleBot('6561545637:AAFgVEB-kK92iG5-bYLysYg8sSIGGqH0ur8')

@botArg.message_handler()
def roflophoto(message):
    photo = open('/Users/guusarskiy/Downloads/IMG_2885.jpg', 'rb')

    if (message.from_user.id != kosarID):
        botArg.reply_to(message, 'опа наебочка))))))')
        botArg.send_photo(message.chat.id, photo)

@botArg.message_handler(commands=['create'])
def create(message):
    if (message.from_user.id == kosarID):
        global currentID
        currentID = message.from_user.id

        """conn = psycopg2.connect(host='localhost', dbname='betbot', user='postgres', password='TxpFH44T', port=5433)
        cur = conn.cursor()
        cur.execute('create table if not exists events(id integer primary key, event_description text, bet_cf numeric(10, 2) default 1.00)')
        cur.execute('create table if not exists users(id integer, name varchar(30) unique, event_id integer references events (id), bet_value integer)')
        conn.commit()
        cur.close()
        conn.close()"""

        botArg.reply_to(message,
                        'Введите два исхода через запятую (БЕЗ ПРОБЕЛА МЕЖДУ НИМИ, ПРОБЕЛЫ ДОПУСКАЮТСЯ В ОПИСАНИИ ИСХОДОВ СОБЫТИЯ) в формате: <исход1>,<исход2>')
        botArg.register_next_step_handler(message, create_bet)


def create_bet(message):
    global currentID
    #input_type = '<class \'str\'>'

    if (message.from_user.id == currentID):
        if (message.text == '/stop'):
            return

        conn = psycopg2.connect(host='localhost', dbname='betbot', user='postgres', password='TxpFH44T', port=5432)
        cur = conn.cursor()

        try:
            cur.execute(
                'create table if not exists events(id integer primary key, event_description text, bet_cf numeric(10, 2) default 1.00)')
            cur.execute(
                'create table if not exists users(id integer, name varchar(30), event_id integer references events (id), bet_value integer)')

            eventList = []
            eventList = message.text.split(',')
            firstEvent = eventList[0]
            secondEvent = eventList[1]

            cur.execute('insert into events (id, event_description) values ({}, \'{}\');'.format(1, firstEvent))
            cur.execute('insert into events (id, event_description) values ({}, \'{}\');'.format(2, secondEvent))
            conn.commit()
            cur.close()
            conn.close()

            """
            if ((str(type(firstEvent)) == input_type) and (str(type(secondEvent)) == input_type)):
                botArg.reply_to(message, 'Событие зарегестрировано!')
            else:
                botArg.reply_to(message, 'Неправильный формат ввода!')"""
            botArg.reply_to(message, 'Событие зарегестрировано!')
        except Exception:
            botArg.reply_to(message, 'ОШИБКА при создании события! Вероятно, такое событие уже существует')
    else:
        botArg.send_message(message.chat.id, 'Жду ответа от {}'.format(currentID))
        botArg.register_next_step_handler(message, create_bet)


@botArg.message_handler(commands=['bet'])
def bet(message):
    global currentID
    global currentNAME
    currentID = message.from_user.id
    currentNAME = "@" + message.from_user.username

    botArg.reply_to(message,
                    'Введите ФИО, номер исхода, размер ставки через запятую (БЕЗ ПРОБЕЛА МЕЖДУ НИМИ, ПРОБЕЛЫ ДОПУСКАЮТСЯ В ПЕРЕМЕННОЙ ФИО) в формате: <ФИО>,<исход>,<ставка>')
    botArg.register_next_step_handler(message, insert_bet)


def insert_bet(message):
    global currentID
    global currentNAME
    #currentNAME = "@" + message.from_user.username
    #input_type = '<class \'str\'>'

    if (message.from_user.id == currentID):
        if (message.text == '/stop'):
            return

        conn = psycopg2.connect(host='localhost', dbname='betbot', user='postgres', password='TxpFH44T', port=5432)
        cur = conn.cursor()

        try:
            bet_list = []
            bet_list = message.text.split(',')
            user_fio = bet_list[0]
            user_event = bet_list[1]
            user_bet = int(bet_list[2])
        except Exception:
            botArg.reply_to(message, 'ОШИБКА в формате ввода')

        try:
            cur.execute(
                'insert into users (id, name, event_id, bet_value) values ({}, \'{}\', \'{}\', {});'.format(currentID,
                                                                                                            user_fio,
                                                                                                            user_event,
                                                                                                            user_bet))
            conn.commit()

            # sum_list = ()

            cur.execute('select sum(bet_value) from users where event_id = 1')
            sum_list = cur.fetchall()
            str_help = ''.join(map(str, sum_list))
            str_help = str_help.replace('(', '')
            str_help = str_help.replace(')', '')
            str_help = str_help.replace(',', '')
            if (str_help == 'None'):
                str_help = '0'
            str_arg1 = str_help
            # botArg.send_message(message.chat.id, str_arg1)

            cur.execute('select sum(bet_value) from users where event_id = 2')
            sum_list = cur.fetchall()
            str_help = ''.join(map(str, sum_list))
            str_help = str_help.replace('(', '')
            str_help = str_help.replace(')', '')
            str_help = str_help.replace(',', '')
            if (str_help == 'None'):
                str_help = '0'
            str_arg2 = str_help
            # botArg.send_message(message.chat.id, str_arg2)

            str_summ = 0
            str_summ = (int(str_arg1) + int(str_arg2))
            # botArg.send_message(message.chat.id, str(str_summ))

            sum_event1 = int(str_arg1)
            sum_event2 = int(str_arg2)
            final_cf_event1 = 1
            final_cf_event2 = 1

            if (sum_event2 == 0):
                cf_event1 = ((sum_event2 / sum_event1) + 1)
                final_cf_event1 = math.floor(cf_event1 * 100) / 100

                cf_event2 = 1
                final_cf_event2 = 1

            elif (sum_event1 == 0):
                cf_event1 = 1
                final_cf_event1 = 1

                cf_event2 = ((sum_event1 / sum_event2) + 1)
                final_cf_event2 = math.floor(cf_event2 * 100) / 100

            else:
                cf_event1 = ((sum_event2 / sum_event1) + 1)
                final_cf_event1 = math.floor(cf_event1 * 100) / 100

                cf_event2 = ((sum_event1 / sum_event2) + 1)
                final_cf_event2 = math.floor(cf_event2 * 100) / 100

            cur.execute('update events set bet_cf = {} where id = 1'.format(final_cf_event1))
            cur.execute('update events set bet_cf = {} where id = 2'.format(final_cf_event2))
            conn.commit()

            cur.close()
            conn.close()

            botArg.reply_to(message, 'Ставка зарегестрирована!')

            conn = psycopg2.connect(host='localhost', dbname='betbot', user='postgres', password='TxpFH44T', port=5432)
            cur = conn.cursor()

            cur.execute('select event_description from events where id = 1')
            sum_list = cur.fetchall()
            str_help = ''.join(map(str, sum_list))
            str_help = str_help.replace('(', '')
            str_help = str_help.replace(')', '')
            str_help = str_help.replace(',', '')
            # str_help = str_help.replace('\'', '')
            str_event1 = str_help
            # botArg.send_message(message.chat.id, str_event1)

            cur.execute('select event_description from events where id = 2')
            sum_list = cur.fetchall()
            str_help = ''.join(map(str, sum_list))
            str_help = str_help.replace('(', '')
            str_help = str_help.replace(')', '')
            str_help = str_help.replace(',', '')
            # str_help = str_help.replace('\'', '')
            str_event2 = str_help
            # botArg.send_message(message.chat.id, str_event2)

            cur.execute('select bet_cf from events where id = 1')
            sum_list = cur.fetchall()
            str_help = ''.join(map(str, sum_list))
            str_help = str_help.replace('(', '')
            str_help = str_help.replace(')', '')
            str_help = str_help.replace(',', '')
            str_help = str_help.replace('\'', '')
            str_help = str_help.replace('Decimal', '')
            str_cf1 = str_help
            # botArg.send_message(message.chat.id, str_cf1)

            cur.execute('select bet_cf from events where id = 2')
            sum_list = cur.fetchall()
            str_help = ''.join(map(str, sum_list))
            str_help = str_help.replace('(', '')
            str_help = str_help.replace(')', '')
            str_help = str_help.replace(',', '')
            str_help = str_help.replace('\'', '')
            str_help = str_help.replace('Decimal', '')
            str_cf2 = str_help
            # botArg.send_message(message.chat.id, str_cf2)

            cur.execute('select users.name, users.bet_value from users where event_id = 1')
            test_list = cur.fetchall()
            info_users1 = ''
            for item in test_list:
                info_users1 += f'{item[0]}: {item[1]}\n'
            # botArg.send_message(message.chat.id, info_users)

            cur.execute('select users.name, users.bet_value from users where event_id = 2')
            test_list = cur.fetchall()
            info_users2 = ''
            for item in test_list:
                info_users2 += f'{item[0]}: {item[1]}\n'
            # botArg.send_message(message.chat.id, info_users)

            # str_info = f'Исход 1: {str_event1}, коэф. - {str_cf1}\n{info_users1}\n#########\n\nИсход 2: {str_event2}, коэф. - {str_cf2}\n{info_users2}'
            botArg.send_message(message.chat.id,
                                f'<u><b>Исход 1: <i>{str_event1}</i>\nКоэффициент: <i>{str_cf1}</i></b></u>\n<i>{info_users1.title()}</i>\n<u><b>Исход 2: <i>{str_event2}</i>\nКоэффициент: <i>{str_cf2}</i></b></u>\n<i>{info_users2.title()}</i>',
                                parse_mode='html')

            conn.commit()
            cur.close()
            conn.close()
        except Exception:
            botArg.reply_to(message, 'ОШИБКА при обработке ставки! Проверьте формат ввода/ставили ли вы раньше. Если вы уже ставили на этот исход, можно добавить сумму через /add. В противном случае, заново напишите /bet')
    else:
        #_username = message.from_user.username
        #botArg.send_message(message.chat.id, 'Жду ответа от {}'.format(currentID))
        botArg.send_message(message.chat.id, 'Жду ответа от {}'.format(currentNAME))
        botArg.register_next_step_handler(message, insert_bet)


@botArg.message_handler(commands=['info'])
def info(message):
    conn = psycopg2.connect(host='localhost', dbname='betbot', user='postgres', password='TxpFH44T', port=5432)
    cur = conn.cursor()

    cur.execute('select event_description from events where id = 1')
    sum_list = cur.fetchall()
    str_help = ''.join(map(str, sum_list))
    str_help = str_help.replace('(', '')
    str_help = str_help.replace(')', '')
    str_help = str_help.replace(',', '')
    # str_help = str_help.replace('\'', '')
    str_event1 = str_help
    # botArg.send_message(message.chat.id, str_event1)

    cur.execute('select event_description from events where id = 2')
    sum_list = cur.fetchall()
    str_help = ''.join(map(str, sum_list))
    str_help = str_help.replace('(', '')
    str_help = str_help.replace(')', '')
    str_help = str_help.replace(',', '')
    # str_help = str_help.replace('\'', '')
    str_event2 = str_help
    # botArg.send_message(message.chat.id, str_event2)

    cur.execute('select bet_cf from events where id = 1')
    sum_list = cur.fetchall()
    str_help = ''.join(map(str, sum_list))
    str_help = str_help.replace('(', '')
    str_help = str_help.replace(')', '')
    str_help = str_help.replace(',', '')
    str_help = str_help.replace('\'', '')
    str_help = str_help.replace('Decimal', '')
    str_cf1 = str_help
    # botArg.send_message(message.chat.id, str_cf1)

    cur.execute('select bet_cf from events where id = 2')
    sum_list = cur.fetchall()
    str_help = ''.join(map(str, sum_list))
    str_help = str_help.replace('(', '')
    str_help = str_help.replace(')', '')
    str_help = str_help.replace(',', '')
    str_help = str_help.replace('\'', '')
    str_help = str_help.replace('Decimal', '')
    str_cf2 = str_help
    # botArg.send_message(message.chat.id, str_cf2)

    cur.execute('select users.name, users.bet_value from users where event_id = 1')
    test_list = cur.fetchall()
    info_users1 = ''
    for item in test_list:
        info_users1 += f'{item[0]}: {item[1]}\n'
    # botArg.send_message(message.chat.id, info_users)

    cur.execute('select users.name, users.bet_value from users where event_id = 2')
    test_list = cur.fetchall()
    info_users2 = ''
    for item in test_list:
        info_users2 += f'{item[0]}: {item[1]}\n'
    # botArg.send_message(message.chat.id, info_users)

    # str_info = f'Исход 1: {str_event1}, коэф. - {str_cf1}\n{info_users1}\n#########\n\nИсход 2: {str_event2}, коэф. - {str_cf2}\n{info_users2}'
    botArg.send_message(message.chat.id,
                        f'<b>СПИСОК УЧАСТНИКОВ</b>\n\n<u><b>Исход 1: <i>{str_event1}</i>\nКоэффициент: <i>{str_cf1}</i></b></u>\n<i>{info_users1.title()}</i>\n<u><b>Исход 2: <i>{str_event2}</i>\nКоэффициент: <i>{str_cf2}</i></b></u>\n<i>{info_users2.title()}</i>',
                        parse_mode='html')

    conn.commit()
    cur.close()
    conn.close()


@botArg.message_handler(commands=['check'])
def check(message):
    global currentID
    currentID = message.from_user.id

    botArg.reply_to(message,
                    'Введите номер исхода, размер ставки через запятую (БЕЗ ПРОБЕЛА МЕЖДУ НИМИ в формате: <исход>,'
                    '<ставка>')
    botArg.register_next_step_handler(message, checkmate)


def checkmate(message):
    global currentID

    if (message.from_user.id == currentID):
        if (message.text == '/stop'):
            return

        conn = psycopg2.connect(host='localhost', dbname='betbot', user='postgres', password='TxpFH44T', port=5432)
        cur = conn.cursor()
        try:
            bet_list = message.text.split(',')
            # user_fio = bet_list[0]
            user_event = str(bet_list[0])
            user_bet = int(bet_list[1])
        except Exception:
            botArg.reply_to(message, 'ОШИБКА в формате ввода')

        try:
            cur.execute('select sum(bet_value) from users where event_id = 1')
            sum_list = cur.fetchall()
            str_help = ''.join(map(str, sum_list))
            str_help = str_help.replace('(', '')
            str_help = str_help.replace(')', '')
            str_help = str_help.replace(',', '')
            if (str_help == 'None'):
                str_help = '0'
            str_arg1 = str_help
            # botArg.send_message(message.chat.id, str_arg1)

            cur.execute('select sum(bet_value) from users where event_id = 2')
            sum_list = cur.fetchall()
            str_help = ''.join(map(str, sum_list))
            str_help = str_help.replace('(', '')
            str_help = str_help.replace(')', '')
            str_help = str_help.replace(',', '')
            if (str_help == 'None'):
                str_help = '0'
            str_arg2 = str_help
            # botArg.send_message(message.chat.id, str_arg2)

            str_summ = 0
            str_summ = (int(str_arg1) + int(str_arg2) + user_bet)
            # botArg.send_message(message.chat.id, str(str_summ))

            sum_event1 = int(str_arg1)
            sum_event2 = int(str_arg2)
            final_cf_event1 = 1
            final_cf_event2 = 1

            if user_event == '1':
                sum_event1 = int(str_arg1) + user_bet
            elif user_event == '2':
                sum_event2 = int(str_arg2) + user_bet

            if sum_event2 == 0:
                cf_event1 = ((sum_event2 / sum_event1) + 1)
                final_cf_event1 = math.floor(cf_event1 * 100) / 100

                cf_event2 = 1
                final_cf_event2 = 1

            elif sum_event1 == 0:
                cf_event1 = 1
                final_cf_event1 = 1

                cf_event2 = ((sum_event1 / sum_event2) + 1)
                final_cf_event2 = math.floor(cf_event2 * 100) / 100

            else:
                cf_event1 = ((sum_event2 / sum_event1) + 1)
                final_cf_event1 = math.floor(cf_event1 * 100) / 100

                cf_event2 = ((sum_event1 / sum_event2) + 1)
                final_cf_event2 = math.floor(cf_event2 * 100) / 100

            botArg.reply_to(message, f'Коэффицент после вашей ставки будет равен - {final_cf_event1}')
            botArg.reply_to(message, f'Коэффицент после вашей ставки будет равен - {final_cf_event2}')
        except Exception:
            botArg.reply_to(message, 'ОШИБКА при вызове /check. Проверьте формат ввода данных!')

    else:
        botArg.send_message(message.chat.id, 'Жду ответа от {}'.format(currentID))
        botArg.register_next_step_handler(message, checkmate)


@botArg.message_handler(commands=['droptb'])
def droptb(message):
    try:
        if ((message.from_user.id == kosarID) or (message.from_user.id == lemenkoID) or (message.from_user.id == sozikID)):
            conn = psycopg2.connect(host='localhost', dbname='betbot', user='postgres', password='TxpFH44T', port=5432)
            cur = conn.cursor()
            cur.execute('drop table users;')
            cur.execute('drop table events;')
            conn.commit()
            cur.close()
            conn.close()

            botArg.reply_to(message, 'Событие удалено!')
    except Exception:
        botArg.reply_to(message, 'ОШИБКА при удалении события. Вероятно, такого события не существует!')


botArg.infinity_polling()

"""
@botArg.message_handler()
def roflophoto(message):
    photo = open('/Users/mac/Downloads/EmL_CITUQVE.jpg', 'rb')

    if (message.from_user.id == sozikID):
        botArg.reply_to(message, 'Твоя любимая)))))))')
        botArg.send_photo(message.chat.id, photo)
"""
"""def user_bet(message):
    global betSql
    betSql = int(message.text.strip())

    conn = psycopg2.connect(host='localhost', dbname='betbot', user='postgres', password='TxpFH44T', port=5433)
    cur = conn.cursor()

    cur.execute('insert into users (name, bet_value) values (\'{}\', {});'.format(nameSql, betSql))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    botArg.send_message(message.chat.id, 'Все готово!', reply_markup=markup)

def user_output(message):
    if message.text == ('out'):
        conn = psycopg2.connect(host='localhost', dbname='betbot', user='postgres', password='TxpFH44T', port=5433)
        cur = conn.cursor()

        cur.execute('select * from users;')
        users = cur.fetchall()

        # global info
        info = ''
        for item in users:
            info += f'Имя: {item[1]}, Размер ставки: {item[2]}\n'

        cur.close()
        conn.close()

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineQueryResultArticle(info))
        botArg.send_message(message.chat.id, 'Ставки: ', reply_markup=markup)

@botArg.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = psycopg2.connect(host='localhost', dbname='betbot', user='postgres', password='TxpFH44T', port=5433)
    cur = conn.cursor()

    cur.execute('select * from users;')
    users = cur.fetchall()

    #global info
    info = ''
    for item in users:
        info += f'Имя: {item[1]}, Размер ставки: {item[2]}\n'

    cur.close()
    conn.close()

    botArg.send_message(call.message.chat.id, info)"""

'''@botArg.message_handler()
def id(message):
    botArg.reply_to(message, str(message.from_user.id))'''

"""@botArg.message_handler()
def create(message):
    if (message.text.lower() == '/create'):
        botArg.reply_to(message, (message.from_user.id))"""

""""@botArg.message_handler(commands = ['start'])
def main(messageArg):
    botArg.send_message(messageArg.chat.id, f'скам бот активирован! {messageArg.from_user.first_name}, '
                                            f'настоятельно рекомендую отправить админу свой цвв!')

@botArg.message_handler(commands = ['roflan'])
def main(messageArg):
    webbrowser.open('https://altaimag.ru/products/im-krem-persidskij-shah-dlya-muzhchin-50ml/')"""

""""@botArg.message_handler(content_types=['photo'])
def get_photo(messageArg):
    botArg.reply_to(messageArg, 'хуя ты урод')"""
"""
@botArg.message_handler(commands=['buttons'])
def start(messageArg):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('рофлан')
    btn2 = types.KeyboardButton('контент')
    markup.row(btn1, btn2)
    botArg.send_message(messageArg.chat.id, 'asljdhfas', reply_markup=markup)

@botArg.message_handler()
def info(messageArg):
    if (messageArg.text.lower() == 'охуел?'):
        botArg.send_message(messageArg.chat.id, ')))))))')
    if (messageArg.text.lower() == 'мать ебал'):
        botArg.send_message(messageArg.chat.id, 'ээээээээ про мать лишнее!')
    if (messageArg.text.lower() == '/id'):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Переход на сайт',
                                              url='https://altaimag.ru/products/im-krem-persidskij-shah-dlya-muzhchin-50ml/'))
        botArg.reply_to(messageArg, f'Ваш ID: {messageArg.from_user.id}', reply_markup=markup)
    if (messageArg.text.lower() == '/start'):
        botArg.send_message(messageArg.chat.id, f'скам бот активирован! {messageArg.from_user.first_name}, '
                                                f'настоятельно рекомендую отправить админу свой цвв!')

    if (messageArg.text.lower() == '/roflan'):
        webbrowser.open('https://altaimag.ru/products/im-krem-persidskij-shah-dlya-muzhchin-50ml/')
"""

# botArg.polling(none_stop = True)
