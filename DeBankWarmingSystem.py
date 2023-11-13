import random
import sqlite3
import time
import traceback
import uuid
from datetime import datetime, date
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Float, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from DebankModel import *

# Создание базы данных
engine = create_engine('sqlite:///debank_accounts.db')
Base = declarative_base()


# Определение модели данных
class DebankAccount(Base):
    __tablename__ = 'accounts'

    id = Column(String, primary_key=True)
    address = Column(String)
    privateKey = Column(String)
    proxy = Column(String)
    warmingStrick = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    followings = Column(Integer, default=0)
    rank = Column(Integer, default=0)
    balance = Column(Float, default=0)
    TVF = Column(Float, default=0)
    createDate = Column(DateTime, default=datetime.utcnow)
    lastChangeDate = Column(DateTime)


# Создание таблицы в базе данных, если она не существует
if not inspect(engine).has_table(DebankAccount.__tablename__):
    Base.metadata.create_all(engine)

# Создание сессии для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()


def perform_some_operations(account, accounts):

    # print(account.address)
    DB_Account = DeBank({'address': account.address,
                         'private_key': account.privateKey,
                         'proxy': f'http://{account.proxy.split(":")[2]}:{account.proxy.split(":")[3]}@{account.proxy.split(":")[0]}:{account.proxy.split(":")[1]}'})

    time.sleep(random.randint(200,300)/100)
    print('Авторизуюсь')
    DB_Account.Authorize()
    time.sleep(random.randint(500, 700) / 100)

    conn_ = sqlite3.connect('Posts.db', check_same_thread=False)
    cursor_ = conn_.cursor()

    cursor_.execute("""SELECT * FROM posts""")
    posts = cursor_.fetchall()
    #
    # for post in posts:
    #     print(post)

    random_text = random.choice(posts)

    DB_Account.MakePost(random_text[1])
    time.sleep(random.randint(500, 700)/100)

    conn_.close()

    account.followers, account.followings, account.rank, account.balance, account.TVF = DB_Account.GetStats()
    time.sleep(random.randint(500, 700) / 100)

    for i in range(random.randint(1,6)):
        randomAccount = random.choice(accounts)

        DB_Account.Follow(randomAccount.address)
        time.sleep(random.randint(500, 700)/100)

    return account



# Цикл проверки и выполнения определенных функций

if __name__ == '__main__':

    while True:
        today = date.today()

        # print(today)

        # Извлечение аккаунтов, у которых lastChangeDate не совпадает с сегодняшним днем
        accounts = session.query(DebankAccount).filter(DebankAccount.lastChangeDate != today).all()

        if len(accounts) == 0:
            print("Нет аккаунтов для обновления. Продолжаем...")
            time.sleep(5)
            continue

        for account in accounts[24:]:

            try:
                account = perform_some_operations(account, accounts)

                # Обновление lastChangeDate аккаунта
                account.lastChangeDate = today
                account.warmingStrick += 1

                print(account.TVF, account.rank, account.balance)

                session.commit()
            except:
                traceback.print_exc()

            time.sleep(5)


        print("Выполнены операции для всех аккаунтов. Продолжаем...")
        input()

        # Вставьте здесь код для установки интервала ожидания перед следующей проверкой

    # Закрытие сессии
    # session.close()
