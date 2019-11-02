from pprint import pprint
from peewee import JOIN

from infrastructure.relational_db import db
from infrastructure.relational_db.models import Bike, Cart, User

db.connect()

query_01 = Bike \
    .select() \
    .join(Cart, JOIN.LEFT_OUTER) \
    .where(Cart.id != None)
print(query_01.sql())
pprint(len(query_01))


query_02 = Cart \
    .select() \
    .join(Bike) \
    .join_from(Cart, User) \
    .where(Cart.user_id.email == "zeka.rum@gmail.com")
print(query_02.sql())
for res in query_02:
    pprint(res.bike_id)

db.close()
