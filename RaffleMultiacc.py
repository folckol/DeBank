import random
import sqlite3
import time
import traceback
import uuid
from datetime import datetime, date
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Float, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from DeBankModel import *

# Создание базы данных
engine = create_engine('sqlite:///DataBases/debank_accounts.db', pool_size=1000, max_overflow=1000)
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
    count = 0
    while count < 5:
        try:
            DB_Account = DeBank({'address': account.address,
                                 'private_key': account.privateKey,
                                 'proxy': f'http://{account.proxy.split(":")[2]}:{account.proxy.split(":")[3]}@{account.proxy.split(":")[0]}:{account.proxy.split(":")[1]}'})

            # time.sleep(random.randint(200, 300) / 100)
            # print('Авторизуюсь')


            DB_Account.Authorize()
            break
        except:

            time.sleep(random.randint(200, 300) / 100)
            pass

        count+=1

    time.sleep(random.randint(300, 700) / 100)

    DB_Account.Follow('0x08a51a2ea9ab4361b3885145a32e5379b9333ffb')
    time.sleep(random.randint(300, 600) / 100)

    result = DB_Account.JoinLuckyDraw(5677)
    return result


# Цикл проверки и выполнения определенных функций

if __name__ == '__main__':

    accounts = session.query(DebankAccount).all()

    while len(accounts) != 0:

        try:
            r_account = random.choice(accounts)
            result = perform_some_operations(r_account, accounts)

            print(result)
            if result['data']['is_success']:
                print(r_account.address, '-', datetime.utcnow(), '-', 'Success')
            else:
                print(r_account.address, '-', datetime.utcnow(), '-', 'IDK')

            session.commit()

        except Exception as e:

            traceback.print_exc()

            if 'JSONDecodeError' in str(e):
                print(r_account.address, '-', datetime.utcnow(), '-', 'Error')

            else:
                # traceback.print_exc()
                print(r_account.address, '-', datetime.utcnow(), '-', 'Error')
        accounts.remove(r_account)

        time.sleep(random.randint(1, 31))

