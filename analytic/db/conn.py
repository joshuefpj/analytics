from os import environ

db_user = environ.get('postgres_user')
db_pass = environ.get('postgres_pass')
db_name = environ.get('postgres_db')
container = environ.get('postgres_host')


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
