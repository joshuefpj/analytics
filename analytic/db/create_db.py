from conn import Connection
from utils import get_keys
from tables import AccountDetails, TransactionLog

import sqlalchemy as db, create_engine, MetaData
from sqlalchemy.orm import sessionmaker

ENGINE = create_engine('')
meta = MetaData(bind=ENGINE)


def _create_log_table(data_file):
    db_data = get_keys(data_file)
    
    with Connection(**db_data) as conn:
        conn.create_table()


def add_transaction(details):
    with db.create_engine(ENGINE) as engine:
        MetaData.reflect(meta)

        meta.create_all(ENGINE)

        post = TransactionLog.insert().values(**details)
        ENGINE.execute(post)


def get_email_by_account(account):
    query = sqlalchemy.select((
        AccountDetails
    )).filter(AccountDetails.c.account == account)
    
    result = ENGINE.execute(query).fetchone()

    return result


if __name__ == '__main__':
    fl_name = 'data_useless.csv'
    _create_log_table(fl_name)
