from calendar import month_name
from os import environ
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl

from pathlib import Path

from utils import read_file

base_dir = Path(__file__).parents[0]
template_file = base_dir / 'data_collection' / 'template.html'
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
        months_paragraphs += base_p.format(
            month_name[int(k)], v
        )

    return months_paragraphs


def get_image(name) -> bytes:
    """Retrieves the bytes from the file with the image.

    Parameters
    ----------
        name:
            The name for the specific file, without extension(png by
            default).

    Returns
    -------

    """
    file = images_dir / f'{name}.png'

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
    sender_email = environ.get('sender_email', '13.phakman@gmail.com')
    i_key = environ.get('gmail_key', 'uandrpwyzzmwvelt')
    img_logo = get_image('stori_logo')
    account_stats = get_image(account)

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
        message.attach(msgStats)

    # Connection to server
    context = ssl.create_default_context()
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(sender_email, i_key)
        smtp_server.sendmail(
            sender_email, receipt, message.as_string()
        )


if __name__ == '__main__':
    sender = 'd10z.kk@gmail.com'
    acc = '1Q0UTOL'
    a = 4902.42
    b = -3992.23
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
    }
    print(sender)
    send_email(acc, sender, d)
