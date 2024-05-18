from os import environ

db_user = environ.get('POSTGRES_USER', 'higuinho')
db_pass = environ.get('POSTGRES_PASSWORD', 'new_secret_phrase')
db_name = environ.get('POSTGRES_DB', 'transactions')
container = environ.get('POSTGRES_HOS', '172.21.0.2')
# psql -h 172.21.0.2 -p 5432 -U higuinho -d transactions


class Connection:
    def __init__(self):
        self.host = container
        self.port = 5432
        self.dbname = db_name
        self.user_name = db_user
        self.password = db_pass
        self.connection_str = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
            self.user_name,
            self.password,
            self.host,
            self.port,
            self.dbname,
        )
