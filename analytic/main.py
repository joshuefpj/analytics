from check_analysis import get_data, generate_details, file_list
from generate_data import generate_data
from send_email import send_email


if __name__ == '__main__':
    generate_data()
    accs = ['SIO5ZXT']
    account_files = file_list()

    for acc in accs:
        print('ACCOUNT:', acc)
        d = get_data(acc)

        account_details = generate_details(d, acc)

        send_email(acc, '13.phakman@gmail.com', account_details)
