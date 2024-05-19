from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from conn import Connection
from tables import AccountDetails, TransactionLog

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


def validate_account(session: Session, account: str) -> bool:
    """Validates whether the account id already exists or not.

    Parameters
    ----------
        session:
            The session to be used for DB connect.

        account:
            The unique identifier for the account.

    Returns
    -------
        The check for the provided account.
    """
    if not isinstance(account, str):
        return

    email = get_email_by_account(session, account)
    return bool(email)


def get_email_by_account(session: Session, account: str) -> str:
    """Retrieve the email for a particular account from DB.

    Returns
    -------
        Retrieve the engine for DB connection.
    """
    if not isinstance(account, str):
        return

    email = session.query(AccountDetails).filter(
        AccountDetails.account == account
    ).all()

    try:
        return email[0].email
    except IndexError as e:
        print('Account does not exist:', e)
        return 0

def insert_row_orm(
        session: Session,
        table_structure,
        details: dict
    ) -> None:
    """Inserts a new row into the specified table.

    Parameters
    ----------
        session:
            The Session DB object.

        table_structure:
            The table definition to be used.

        details:
            The data mapping for to be inserted into the table.
    """
    dt = table_structure(**details)

    try:
        session.add(dt)
        session.commit()

    except InvalidRequestError:
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
    insert_row_orm(s, AccountDetails, dd)
    e = get_email_by_account(s, dd['account'])

    for a in ['AG133EI0', 'afl', '']:
        a_response = validate_account(s, a)
        print(f'{a}: {a_response}')
