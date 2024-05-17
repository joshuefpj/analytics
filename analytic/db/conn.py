from psycopg2 import connect, sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Connection:
    def __init__(self, host, port, database_name, user, password):
        self.host = host
        self.port = port
        self.dbname = database_name
        self.user_name = user
        self.password = password
    
    def con(self):
        connection = connect(
            dbname=self.dbname,
            user=self.user_name,
            host=self.host,
            password=self.password,
        )

        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        return connection
    
    def create_tables(self):
        c = self.con()

        with c.cursor() as cur:
            sql = """"
            CREATE TABLE account_details (
                account VARCHAR(255) NOT NULL,
                first_name VARCHAR(79) NOT NULL,
                last_name VARCHAR(79),
                email VARCHAR(255) NOT NULL,
                PRIMARY KEY (account)
            )
            """

            cur.execute(sql)

        with c.cursor() as cur:
            sql = """"
            CREATE TABLE transaction_logging (
                id serial, num integer, data varchar,
                log_date TIMESTAMP,
                account VARCHAR(255),
                debit FLOAT,
                credit FLOAT,
                transactions_count INT,
                PRIMARY KEY (id),
                FOREIGN KEY (account) REFERENCES account_details(account)
            )
            """

            cur.execute(sql)
    
    def get_transactions_by_account(self, account):
        # TODO: implement method to retrieve information for an account.
        pass
