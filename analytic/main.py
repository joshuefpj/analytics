from pathlib import Path
from random import choice
import sys, os

project_path = Path(__file__).parents[0]
sys.path.insert(0, os.path.abspath(str(project_path)))

from db.fresh_db import get_email_by_account, insert_row_orm
from db.tables import AccountDetails, TransactionLog
from check_analysis import (
    get_data, generate_details, file_list
)
from generate_data import generate_data
from logging_analytic import Logging
from send_email import send_email

from random import randint

"""This module file will be used to control the flow.

Parameters
----------
    Nothing required.
"""

# Here we need to define the number of files to be generated in every
# execution, and the amount of rows.

Logging(f'Starting job. ({__file__})').info()
row_nums = randint(1309, 1979)
Logging('Generate new file').info()
generate_data(1, row_nums)

# We obtain the list of accounts to be processed.
Logging('Getting file list from data directory.').info()
account_files = file_list()

# We will process each account and send detailed information.
for acc in account_files[:1]:
    names = 'mario luigui koppa harry leonardo leah miguilangel rafael donatello'.split()
    last_name = 'bros turtle peach solo skywalker'.split()

    n = choice(names)
    l = choice(last_name)

    Logging(f'ACCOUNT: {acc}').info()

    d = get_data(acc)

    # Process data.
    account_details = generate_details(d, acc)
    Logging(f'DETAILS: \n{account_details}').info()

    # Create names and emails randomly.
    account_details['account_db'] = {
        'account': acc,
        'email': f'{l.capitalize()}.{n.capitalize()}@noexisto.com',
        'first_name': n,
        'last_name': l,
    }
    # Send email details.
    receipt_email = environ.get('sender_email')
    Logging(f'Send email for account: {acc}').info()
    send_email(acc, receipt_email, account_details)
