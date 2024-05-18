from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
BaseClass = declarative_base()


class AccountDetails(BaseClass):
    __tablename__ = 'account_details'
    account = Column(String, primary_key=True, nullable=False, unique=True)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)


class TransactionLog(BaseClass):
    __tablename__ = 'transaction_logging'
    id = Column(Integer, primary_key=True, nullable=False)
    log_date = Column(DateTime, default=datetime.now)
    account = Column(
        String,
        ForeignKey('account_details.account'),
    )
    debit = Column(Float, nullable=False)
    credit = Column(Float, nullable=False)
    transactions_count = Column(Float, nullable=False)
