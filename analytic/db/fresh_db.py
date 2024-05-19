from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from conn import Connection
from tables import AccountDetails, TransactionLog

con = Connection()
db_conn_str = con.connection_str


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

    email = get_email_by_account(session, account)
    return bool(email)


def get_email_by_account(session, account):
    if not isinstance(account, str):
        return 0

    email = session.query(AccountDetails).filter(
        AccountDetails.account == account
    ).all()

    try:
        return email[0].email
    except IndexError as e:
        print('Account does not exist:', e)
        return 0

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
        'account': 'AG133EI0',
        'email': 'far@noexisto.com',
        'first_name': 'far',
        'last_name': 'dos',
    }

    s = gen_session()
    # insert_row_orm(s, AccountDetails, dd)
    e = get_email_by_account(s, dd['account'])

    for a in ['AG133EI0', 'afl', '']:
        a_response = validate_account(s, a)
        print(f'{a}: {a_response}')
