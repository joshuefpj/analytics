from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

conn_url = 'postgresql+psycopg2://higuinho:new_secret_phrase@172.21.0.2:5432/transactions'

engine = create_engine(conn_url)

db = scoped_session(sessionmaker(bind=engine))


query = db.execute('select * from account_details').fetchall()

for r in query:
    print(r['account'], r['email'], r['first_name'], ['last_name'])