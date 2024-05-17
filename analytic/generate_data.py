from pathlib import Path
from random import randint, choice
from string import ascii_uppercase, digits
import pandas as pd

base_dir = Path(__file__).parents[0]
data_dir = base_dir / 'data_collection'


def _generate_data(user_id: str, rows: int):
    filename = data_dir / f'{user_id}.csv'

    idx = [x for x in range(rows)]
    date_t = [f'{randint(5, 9)}/{randint(1, 30):02}' for _ in range(rows)]
    trx = [randint(3000, 100000) / 100 for _ in range(rows)]

    trx = [x * -1 if bool(randint(0, 1)) else x for x in trx]

    date_t.sort()

    data = pd.DataFrame({
        'id': idx,
        'date': date_t,
        'transaction': trx
    })

    data.to_csv(str(filename), index=False)


def generate_data(accounts: int=1, rows_: int=10):
    for _ in range(accounts):
        acc = ''.join([choice(ascii_uppercase + digits) for _ in range(7)])
        print('Creating file for:', acc)
        _generate_data(acc, rows_)


if __name__ == '__main__':
    acc = ''.join([choice(ascii_uppercase + digits) for _ in range(7)])
    print('ACCOUNT:', acc)
    _generate_data(acc, 10)
