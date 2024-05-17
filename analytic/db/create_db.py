from conn import Connection
from utils import get_keys


def create_log_table(data_file):
    db_data = get_keys(data_file)
    
    with Connection(**db_data) as conn:
        conn.create_table()


if __name__ == '__main__':
    fl_name = 'data_useless.csv'
    create_log_table(fl_name)
