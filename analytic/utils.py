from pathlib import Path

base_dir = Path(__file__).parents[0]


def get_keys(data_file_name):
    data_file = base_dir / 'super_secret_dir' / f'{data_file_name}.csv'
    print('FILE NAME get_k', str(data_file))

    lines = read_file(data_file)

    _data = {x.split(',')[0]: x.strip().split(',')[1] for x in lines}
    
    return _data


def read_file(file_path, as_str=False):
    with open(str(file_path), 'r') as fl:
        lines = fl.readlines()

        if as_str:
            lines = ''.join(lines)

    return lines
