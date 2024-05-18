from dotenv import load_dotenv, find_dotenv

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from conn import Connection
from tables import AccountDetails, TransactionLog

con = Connection()
db_conn_str = con.connection_str
load_dotenv(find_dotenv())

SECRET_KEY = getenv('SECRET_KEY')
DB_USER = getenv('DB_USER')
DB_PASS = getenv('DB_PASSWORD')
DB_NAME = getenv('DB_NAME')
DB_SERVICE = getenv('_SERVICE')
DB_PORT = getenv('DB_PORT')
DP_IP = getenv('DB_IP')


def _connect_db():
    db = create_engine(db_conn_str)

    return db


def gen_session():
    engine = _connect_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def validate_account(session, account):
    if not isinstance(account, str):
        return 0

    count = session.query(AccountDetails).filter(
        AccountDetails.account == account
    ).count()

    return count

def insert_row_orm(session, table_structure, details):
    dt = table_structure(**details)

    try:
        session.add(dt)
        session.commit()

    except IntegrityError:
        print('Identifier already exists.', details)
        return False


if __name__ == '__main__':
    dd = {
        'account': 'AG198EI0',
        'email': 'far@noexisto.com',
        'first_name': 'far',
        'last_name': 'dos',
    }

    s = gen_session()
    insert_row_orm(s, AccountDetails, dd)
