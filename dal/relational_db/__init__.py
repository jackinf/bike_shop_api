from peewee import PostgresqlDatabase

# db = connect(os.environ.get('BIKESHOP_DATABASE') or 'postgresql://postgres:******@localhost:5432/bikeshop')
db = PostgresqlDatabase('bikeshop', user='postgres', password='******', host='localhost', port='5432')
