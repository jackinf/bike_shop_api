import os
from peewee import PostgresqlDatabase
from psycopg2 import connect

conn_string = os.environ.get('BIKESHOP_DATABASE')
if conn_string is None:
    db = PostgresqlDatabase('bikeshop', user='postgres', password='docker', host='localhost', port='5432')
else:
    db = connect(conn_string)  # Example: 'postgresql://postgres:******@localhost:5432/bikeshop'
