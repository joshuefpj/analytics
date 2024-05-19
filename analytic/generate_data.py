from pathlib import Path
from random import randint, choice
from string import ascii_uppercase, digits
import pandas as pd

base_dir = Path(__file__).parents[0]
data_dir = base_dir / 'data_collection'


def _generate_data(user_id: str, rows: int) -> None:
    """Logic on file's generator.

    Parameters
    ----------
        user_id:
            The account identifier for file naming.

        rows:
            Number of rows per file to be generated.
    """

    filename = data_dir / f'{user_id}.csv'

    idx = [x for x in range(rows)]
    date_t = [f'{randint(1, 12)}/{randint(1, 30):02}' for _ in range(rows)]
    trx = [randint(3000, 100000) / 100 for _ in range(rows)]

    trx = [x * -1 if bool(randint(0, 1)) else x for x in trx]

    date_t.sort()

    data = pd.DataFrame({
        'id': idx,
        'date': date_t,
        'transaction': trx
    })

    data.to_csv(str(filename), index=False)


def generate_data(accounts: int=1, rows_: int=10) -> None:
    """Function for file generation, this will load data randomly incluiding:
        - id (This will be a consecutive number)
        - date (In 'MM/DD' format)
        - transaction (a random float number, can be either +/-)

    The name will be a 7 characters length string. Using capital letters and
    numbers.

    Parameters
    ----------
        accounts:
            This will define the amount of account files to be generated.

        rows_:
            The number of rows per file to be used.
    """
    for _ in range(accounts):
        acc = ''.join([choice(ascii_uppercase + digits) for _ in range(7)])
        print('Creating file for:', acc)
        _generate_data(acc, rows_)


if __name__ == '__main__':
    acc = ''.join([choice(ascii_uppercase + digits) for _ in range(7)])
    print('ACCOUNT:', acc)
    _generate_data(acc, 1979)
