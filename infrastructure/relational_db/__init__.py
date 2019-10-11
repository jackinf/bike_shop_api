import os
from peewee import PostgresqlDatabase

conn_string = os.environ.get('BIKESHOP_SQL_DATABASE')  # FORMAT: "database;user;pass;host;port"
if conn_string is None:
    db = PostgresqlDatabase('bikeshop', user='postgres', password='docker', host='localhost', port='5432')
else:
    db_creds = conn_string.split(';')
    db = PostgresqlDatabase(db_creds[0], user=db_creds[1], password=db_creds[2], host=db_creds[3], port=db_creds[4])

    # Another example is to use this:
    # db = connect('postgresql://postgres:******@localhost:5432/bikeshop')
