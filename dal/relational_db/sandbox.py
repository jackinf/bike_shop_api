import random
from pprint import pprint

from dal.relational_db import db
from dal.relational_db.models import BikeType, Bike
from helpers import randomString

db.connect()

Bike.delete().execute()
BikeType.delete().execute()

for i in range(1, 5):
    BikeType(
        title=f"Bike_{i}",
        description=f"Descr_{randomString(10)}",
        stars=random.choice([1, 2, 3, 4, 5])
    ).save()

# Get all bike types from the db and select their title
print('get all bike types')
for bike in BikeType.select():
    print(bike.title)

#  Get a single bike type
print('get bike type 1')
bike_type_01 = BikeType.get(BikeType.title == 'Bike_1')  # or BikeType.select().where(BikeType.title == 'Bike_1').get()

# import a bike item
print('Creating a connection between bike and bike type')
Bike(purchase_price=399, selling_price=399, status_key=0, bike_type_id=bike_type_01.id).save()

# Delete bike type 4
print('Deleting an instance')
BikeType.get(BikeType.title == 'Bike_4').delete_instance()

# Join operations
print('Join operation #1')
query_01 = Bike.select(Bike, BikeType).join(BikeType).prefetch(BikeType)
for result in query_01:
    pprint(result.bike_type_id.title)


query_03 = BikeType.select(BikeType, Bike).join(Bike).prefetch(Bike)
for result in query_03:
    for item in result.bikes:
        pprint(item.selling_price)

# print('Join operation without fk')
# query_02 = BikeType\
#     .select(BikeType, Bike)\
#     .join(Bike, on=(BikeType.id == Bike.bike_type_id), attr='res')
# for result in query_02:
#     print(result)

db.close()