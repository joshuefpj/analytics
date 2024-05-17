from pathlib import Path

base_dir = Path(__file__).parents[0]


def get_keys(data_file_name):
    data_file = base_dir / 'super_secret_dir' / f'{data_file_name}.csv'
    with open(data_file, 'r') as fl:
        lines = fl.readlines()

        _data = {x.split(',')[0]: x.strip().split(',')[1] for x in lines}
    
    return _data
