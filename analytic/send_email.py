from os import environ
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from random import choice
import smtplib, ssl

from logging_analytic import Logging

from utils import read_file
from db.fresh_db import get_email_by_account, insert_row_orm
from db.tables import AccountDetails, TransactionLog

base_dir = Path(__file__).parents[0]
template_file = base_dir / 'base_files' / 'template.html'
images_dir = base_dir / 'statistic_images'


def template_replace(details: dict) -> str:
    """This function will replace each key with it's value within the
    template html file.

    Parameters
    ----------
        details:
            The key-value map for each required value for the account.

    Returns
    -------
        The formatted string message.
    """
    template = template_file

    body = read_file(template, 1)

    for k, v in details.items():
        body = body.replace(k, str(v))

    return body


def get_months_details(months: dict) -> str:
    """A paragraph line per month included in the months.

    Parameters
    ----------
        months:
            This will use the number of the month as key and the amount
            of transactions per month.

    Returns
    -------
        A formatted string containing a message per month.
    """
    base_p = '\n                <p>Number of transactions in {}: <b>{}</b></p>'

    months_paragraphs = ''
    for k, v in months.items():
        months_paragraphs += base_p.format(k, v)

    return months_paragraphs


def get_image(name: str, file_path: Path=None) -> bytes:
    """Retrieves the bytes from the file with the image.

    Parameters
    ----------
        name:
            The name for the specific file, without extension(png by
            default).

        file_path:
            [Optional] set specific path for the file.

    Returns
    -------

    """
    if not file_path:
        file_path = images_dir
    file = file_path / f'{name}.png'

    if file.exists() and file.is_file():
        with open(file, 'rb') as fl:
            data = fl.read()

        return data

    return b''


def send_email(account, receipt, details):
    """Main function to send the formatted message to the receipt email.

    Parameters
    ----------
        account:
            The unique account identifier.

        receipt:
            The email address to sent the email.

        details:
            The key-value map containing the details account.
    """
    # Setting up account.
    sender_email = environ.get('sender_email')
    i_key = environ.get('gmail_secret')

    img_logo = get_image('stori_logo', base_dir / 'base_files')
    Logging(f'New account "{account}", adding to DB.').info()
    account_stats = get_image(account)
    account_email = get_email_by_account(account)
    if account_email:
        receipt = ','.join([receipt, account_email])
    else:
        Logging(f'New account "{account}", adding to DB.').info()
        insert_row_orm(AccountDetails, details['account_db'])

    trx_count = sum(details['MONTH_TRX'].values())

    trx_details = {
        'account': account,
        'credit': details['CREDIT_AMOUNT'],
        'debit': details['DEBIT_AMOUNT'],
        'transactions_count': int(trx_count),
    }
    Logging(f'Add trx for account {account} - BALANCE.').info()
    insert_row_orm(TransactionLog, trx_details)

    subject = f'Summary details for account {account}.'

    message = MIMEMultipart('related')
    message['subject'] = subject
    message['From'] = sender_email
    message['To'] = receipt

    msgA = MIMEMultipart('alternative')
    message.attach(msgA)

    # Adding images and months to details.
    details['MONTHS_P'] = get_months_details(details['MONTH_TRX'])
    histogram = ''
    if account_stats:
        histogram = '<img src="cid:statistics" width="490" height="340">'

    details['HISTOGRAM'] = histogram

    # Add Logo.
    msgLogo = None
    if img_logo:
        msgLogo = MIMEImage(img_logo)
        msgLogo.add_header(
            'Content-Disposition',
            'attachment',
            filename='stori_logo.png'
        )
        msgLogo.add_header('Content-ID', '<logo>')

    # Add Statistics.
    msgStats = None
    if account_stats:
        msgStats = MIMEImage(account_stats)
        msgStats.add_header('Content-ID', '<statistics>')
        msgLogo.add_header(
            'Content-Disposition',
            'attachment',
            filename=f'{account}_stats.png'
        )

    html = template_replace(details)
    html_part = MIMEText(html, 'html')

    # Build body message.
    msgA.attach(html_part)
    if msgLogo:
        message.attach(msgLogo)
    if msgStats:
        Logging('Attached statistics graphic.').info()
        message.attach(msgStats)

    # Connection to server
    context = ssl.create_default_context()
    Logging('Sending email in html format.').info()
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(sender_email, i_key)
        smtp_server.sendmail(
            sender_email, receipt, message.as_string()
        )


if __name__ == '__main__':
    names = 'mario luigui koppa harry leonardo leah miguilangel rafael donatello'.split()
    last_name = 'bros turtle peach solo skywalker'.split()
    sender = 'd10z.kk@gmail.com'
    acc = 'PKZKL0L'
    a = 4902.42
    b = -3992.23
    n = choice(names)
    l = choice(last_name)
    d = {
        'TOTAL_BALANCE': a + b,
        'CREDIT_AMOUNT': a / 491,
        'DEBIT_AMOUNT': b / 340,
        'MONTH_TRX': {
            '5': 265,
            '6': 271,
            '7': 303,
            '8': 265,
            '9': 275
        },
        'account_db': {
            'account': acc,
            'email': f'{l.capitalize()}.{n.capitalize()}@noexisto.com',
            'first_name': n,
            'last_name': l,
        }
    }
    send_email(acc, sender, d)
