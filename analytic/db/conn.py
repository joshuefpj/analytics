from os import environ

db_user = environ.get('POSTGRES_USER')
db_pass = environ.get('POSTGRES_PASSWORD')
db_name = environ.get('POSTGRES_DB')
container = environ.get('POSTGRES_HOS')


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
