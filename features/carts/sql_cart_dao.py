import random
from datetime import datetime
from peewee import JOIN
from infrastructure.relational_db import db
from infrastructure.relational_db.models import Bike, BikeType, User, BikeStatus, Cart
from features.bikes.bike_dao import CartDao
from decorators.async_wrapper import async_wrapper
from helpers import from_date_to_str

class SqlCartDao(CartDao):
    def __enter__(self):
        db.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        db.close()

    async def get_single_cart(self, cart_id):
        pass

    async def get_single_bike(self, bike_id):  # TODO: Move to BikeDao
        pass

    async def get_items_from_cart(self, cart_id):
        pass

    async def find_single_cart(self, email):
        pass

    async def find_single_item_in_cart(self, items_in_cart, bike_key):
        pass

    async def add_item_into_cart(self, cart_id, document):
        pass

    async def delete_single_item_from_cart(self, cart_id, bike_id):
        pass