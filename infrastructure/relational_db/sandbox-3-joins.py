from pprint import pprint

from peewee import JOIN

from infrastructure.relational_db import db
from infrastructure.relational_db.models import Bike, Cart, User

db.connect()

query_01 = Bike \
    .select() \
    .join_from(Bike, Cart, JOIN.LEFT_OUTER) \
    .join(User) \
    .where(Cart.id != None and Cart.user_id.email != 'zeka.rum@gmail.com')
print(query_01.sql())
pprint(len(query_01))

# query_02 = Cart \
#     .select() \
#     .join_from(Cart, Bike, JOIN.LEFT_OUTER) \
#     .join_from(Cart, User, JOIN.LEFT_OUTER) \
#     .where()

db.close()
