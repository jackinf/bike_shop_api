from peewee import JOIN

from infrastructure.relational_db import db
from infrastructure.relational_db.models import User, Bike, BikeType, CartItem, BikeStatus

db.connect()

query = Bike.select(Bike, BikeType, CartItem) \
    .join(BikeType, JOIN.LEFT_OUTER, on=(Bike.bike_type == BikeType.id)) \
    .join(User, JOIN.LEFT_OUTER, on=(Bike.user_id == User.id)) \
    .join(BikeStatus, JOIN.LEFT_OUTER, on=(Bike.status_key == BikeStatus.the_key)) \
    .join_from(Bike, CartItem, JOIN.LEFT_OUTER)

print(query.sql())

db.close()