from datetime import datetime

from exceptions import ItemNotFoundException
from infrastructure.relational_db import db
from infrastructure.relational_db.models import Bike, User, Cart
from features.carts.cart_dao import CartDao
from decorators.async_wrapper import async_wrapper

class SqlCartDao(CartDao):
    def __enter__(self):
        db.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        db.close()

    @async_wrapper
    def get_single_cart(self, user_id, bike_id):
        single_cart_query = Cart \
            .select() \
            .where(Cart.user_id == user_id and Cart.bike_id == bike_id) \
            .limit(1)
        if len(single_cart_query) == 0:
            raise ItemNotFoundException()
        return single_cart_query[0]

    @async_wrapper
    def get_items_from_cart(self, user_id, bike_id):
        get_items_query = Cart \
            .select() \
            .join(Bike) \
            .join_from(Cart, User) \
            .where(Cart.user_id == user_id and Cart.bike_id == bike_id)
        bikes = [cart.bike_id for cart in get_items_query]
        return bikes

    @async_wrapper
    def find_single_cart(self, email):
        single_cart_query = Cart \
            .select() \
            .join(User) \
            .where(Cart.user_id.email == email) \
            .limit(1)
        if len(single_cart_query) == 0:
            raise ItemNotFoundException("cart")
        return single_cart_query[0]

    @async_wrapper
    def find_single_item_in_cart(self, cart_id, bike_id):
        single_item_in_cart_query = Cart \
            .select() \
            .join(Bike) \
            .where(Cart.id == cart_id and Cart.bike_id == bike_id) \
            .limit(1)
        if len(single_item_in_cart_query) == 0:
            raise ItemNotFoundException("single item in cart")
        return single_item_in_cart_query[0].bike_id

    @async_wrapper
    def add_item_into_cart(self, email, bike_id):
        if len(Bike.where(Bike.id == bike_id).limit(1)) == 0:
            raise ItemNotFoundException("bike")
        single_user_query = User.where(User.email == email).limit(1)
        if len(single_user_query) == 0:
            raise ItemNotFoundException("user")
        user = single_user_query[0]
        Cart.create(user_id=user.id, bike_id=bike_id, created_on=datetime.now(tz=None))

    @async_wrapper
    def delete_single_item_from_cart(self, cart_id):
        Cart.delete_by_id(cart_id)