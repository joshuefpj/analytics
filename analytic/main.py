from db.fresh_db import get_email_by_account, insert_row_orm
from db.tables import AccountDetails, TransactionLog
from check_analysis import get_data, generate_details, file_list
from generate_data import generate_data
from send_email import send_email

from random import randint

"""This module file will be used to control the flow.

Parameters
----------
    Nothing required.
"""

# Here we need to define the number of files to be generated in every
# execution, and the amount of rows.
row_nums = randint(1309, 1979)
generate_data(1, row_nums)

# We obtain the list of accounts to be processed.
account_files = file_list()

# We will process each account and send detailed information.
for acc in account_files:
    print('ACCOUNT:', acc)
    d = get_data(acc)

    # Process data.
    account_details = generate_details(d, acc)
    print(account_details)

    # Save info in Database.
    if get_email_by_account(acc):
        account_orm = AccountDetails()
        transaction_orm = TransactionLog()

    # Send email details.
    send_email(acc, '13.phakman@gmail.com', account_details)
