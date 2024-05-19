from calendar import month_name
from datetime import datetime, timedelta
from os import listdir
from os.path import getmtime, isfile, join
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd
from pathlib import Path

base_dir = Path(__file__).parents[0]
img_dir = base_dir / 'statistic_images'
data_dir = base_dir / 'data_collection'



def get_plot(credit: pd.DataFrame, debit: pd.DataFrame, account: str) -> None:
    """Generate the plot for both, credit and debit.

    Parameters
    ----------
        credit:
            The table containing the credit transaction details.

        debit:
            The table containing the debit transaction details.

        account:
            The Unique account identifier.
    """
    filename = img_dir / f'{account}.png'

    values = [month_name[x] for x in range(1, 13)]
    #                  if x in credit['month'].unique() or x in debit['month'].unique()]
    plt.rcParams['axes.edgecolor'] = '#fff'
    fig, ax = plt.subplots(figsize=(8,4))

    ax.plot(
        credit['month'], credit['sum'], color='#40F808', linewidth=1.3, ls='-', marker='o', markersize=2.3,
    )
    ax.plot(
        debit['month'], debit['sum'], color='#F81C08', linewidth=1.3, ls='-', marker='o', markersize=2.3,
    )

    # Formatting plot.
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel(' Transaction Date', color='#fff')
    ax.set_ylabel('Amount', color='#fff')
    ax.set_title('Credit/Debit', color='#fff')
    ax.xaxis.set_ticks([x for x in range(1, 13)])
    ax.xaxis.set_ticklabels(values, color='#fff')
    ax.tick_params(axis='y', colors='#fff')
    ax.yaxis.set_ticks_position('left')

    ax.legend(
        ['credit', 'debit'],
        labelcolor='linecolor',
        facecolor='#003A40',
        bbox_to_anchor=(1.0, 1.17),
        ncol=2,
    )

    # plt.show()
    fig.savefig(
        fname=str(filename),
        format='png',
        transparent=True,
    )


def file_list() -> list:
    """Check for files in `path_base` location.

    Returns
    -------
        Account for each valid file founded in `path_base` directory.
    """
    path_base = str(data_dir)
    files_available = [f for f in listdir(path_base) if isfile(join(path_base, f))]

    results = []
    for k in files_available:
        file_mod = getmtime(f'{path_base}/{k}')
        if get_last_run(file_mod) and k.endswith('.csv'):
            results.append(k.split('.')[0])
    
    return results


def get_yesterday_run(file_time: float) -> bool:
    """Same as `get_last_run` but instead of checking for latest 30 mins,
    this will check for the previous 24 hours.

    Setting the specific time in order to don't miss any possible file.
    """
    yesterday = datetime.now() - timedelta(1)
    yesterday = yesterday.replace(hour=9, minute=0, second=0, microsecond=0)

    return yesterday.timestamp() < file_time


def get_last_run(file_time: float) -> bool:
    """This is supposed to run every 30 mins. To avoid all the files gets
    processed every time, we validate for those which were modified within
    previous 30 mins.

    Parameters
    ----------
        file_time:
            The last modification time for the file.

    Returns
    -------
        Return if the time match the modification rules.
    """
    previous_run = datetime.now().timestamp()
    previous_run -= 1800

    return previous_run < file_time


def get_data(account_file: str) -> pd.DataFrame:
    """Reads csv file bassed on user_id naming.

    Parameters
    ----------
        account_file:
            Account unique identifier.

    Returns
    -------
        The transaction table for the account.
    """
    filename = data_dir / f'{account_file}.csv'
    data = pd.read_csv(str(filename))

    return data


def generate_details(raw_data: pd.DataFrame, account: str) -> dict:
    """Main function to generate analysis and retrieve details for particular
    account.
    This dataframe needs to contain below columns:
        - transaction
        - date

    Parameters
    ----------
        raw_data:
            Table with transactions details.

        account:
            The account identifier.

    Returns
    -------
        A key-map structure with account information's details.
    """
    total = raw_data['transaction'].sum()
    per_month = {}
    results = {}

    raw_data['credit'] = raw_data['transaction'].apply(lambda x: 'credit' if x > 0 else 'debit')
    raw_data['month'] = raw_data['date'].apply(lambda x: int(x.split('/')[0]))

    for k in raw_data['month'].unique():
        per_month[month_name[k]] = raw_data[raw_data['month'] == k]['month'].count()
    
    amounts = raw_data.groupby(['month', 'credit'])['transaction'].agg(['sum', 'count'])
    amounts = amounts.reset_index()
    average = raw_data.groupby(['credit'])['transaction'].agg(['sum', 'count'])
    average['average'] = average['sum'] / average['count']

    results['TOTAL_BALANCE'] = total
    results['DEBIT_AMOUNT'] = average.loc['debit']['average']
    results['CREDIT_AMOUNT'] = average.loc['credit']['average']
    results['MONTH_TRX'] = per_month

    data_credit = amounts[amounts['credit'] == 'credit'][['month', 'sum']]
    data_debit = amounts[amounts['credit'] == 'debit'][['month', 'sum']]
    get_plot(
        data_credit, data_debit, account.split('.')[0]
    )

    return results


if __name__ == '__main__':
    # account_files = file_list()
    # print(account_files)
    acc = 'BV1AYJN'
    d = get_data(acc)
    # print(d)

    f = generate_details(d, acc)
    # print(f)
    # my_path_base = '/Users/phakman/repos/analytics/analytic/'
    # file_list(my_path_base)

    # dx = [x / 10 for x in range(0, 100, 5)]
    # c = {'x': dx, 'y': list(map(lambda x: x ** 2, dx))}
    # d = {'x': dx, 'y': list(map(lambda x: x ** 3, dx))}
    # get_plot(c, d)
