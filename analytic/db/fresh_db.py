from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import InvalidRequestError, DataError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
try:
    from logging_analytic import Logging
except ModuleNotFoundError:
    from ..logging_analytic import Logging
from .conn import Connection
from .tables import AccountDetails, TransactionLog

con = Connection()
db_conn_str = con.connection_str


def _connect_db() -> Engine:
    """Generates a DB object.

    Returns
    -------
        Retrieve the engine DB object.
    """
    db = create_engine(db_conn_str)

    return db


def gen_session() -> Session:
    """Generates a DB object.

    Returns
    -------
        Retrieve the session DB object.
    """
    engine = _connect_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def validate_account(account: str) -> bool:
    """Validates whether the account id already exists or not.

    Parameters
    ----------
        account:
            The unique identifier for the account.

    Returns
    -------
        The check for the provided account.
    """
    if not isinstance(account, str):
        return

    email = get_email_by_account(account)
    return bool(email)


def get_email_by_account(account: str) -> str:
    """Retrieve the email for a particular account from DB.

    Returns
    -------
        Retrieve the engine for DB connection.
    """
    session = gen_session()
    if not isinstance(account, str):
        return

    email = session.query(AccountDetails).filter(
        AccountDetails.account == account
    ).all()

    try:
        return email[0].email
    except IndexError as e:
        Logging(f'Account does not exist: {account} {e}').warning()
        return 0

def insert_row_orm(
        table_structure,
        details: dict
    ) -> None:
    """Inserts a new row into the specified table.

    Parameters
    ----------
        table_structure:
            The table definition to be used.

        details:
            The data mapping for to be inserted into the table.
    """
    session = gen_session()
    dt = table_structure(**details)

    try:
        session.add(dt)
        session.commit()

    except InvalidRequestError as ex:
        Logging(f'Identifier already exists: {details}').warning()
        return False
    except DataError as ex:
        Logging(f'Incorrect data: {ex}').warning()


if __name__ == '__main__':
    dd = {
        'account': 'AG133EI0',
        'email': 'far@noexisto.com',
        'first_name': 'far',
        'last_name': 'dos',
    }

    trx_row = {
        'log_date': datetime(2024, 5, 19, 0, 48, 2, 66505),
        'account': 'MBCBLOS',
        'debit': -532.9149066666666,
        'credit': 508.93440874035986,
        'transactions_count': 1528,
    }

    s = gen_session()
    insert_row_orm(TransactionLog, trx_row)
    # e = get_email_by_account(s, dd['account'])

    for a in ['MBCBLOS', 'AG133EI0', 'afl', '']:
        a_response = validate_account(a)
        Logging(f'{a}: {a_response}').info()
