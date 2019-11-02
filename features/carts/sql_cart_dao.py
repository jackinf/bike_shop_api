from datetime import datetime

from exceptions import ItemNotFoundException
from infrastructure.relational_db import db
from infrastructure.relational_db.models import User, CartItem
from features.carts.cart_dao import CartDao
from decorators.async_wrapper import async_wrapper


class SqlCartDao(CartDao):
    def __enter__(self):
        db.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        db.close()

    @async_wrapper
    def dao_get_single_cart(self, user_id, bike_id):
        single_cart_query = CartItem \
            .select() \
            .where(CartItem.user_id == user_id and CartItem.bike_id == bike_id) \
            .limit(1)
        if len(single_cart_query) == 0:
            raise ItemNotFoundException()
        return {
            "cart_id": str(single_cart_query[0].id)
        }

    @async_wrapper
    def dao_get_items_from_cart(self, user_id):
        get_items_query = CartItem \
            .select() \
            .join_from(CartItem, User) \
            .where(CartItem.user_id == user_id)
        return [{
            "bike_id": str(cart.bike_id.id)
        } for cart in get_items_query]


    @async_wrapper
    def dao_find_single_item_in_cart(self, cart_item_id):
        single_item_in_cart_query = CartItem \
            .select() \
            .where(CartItem.id == cart_item_id) \
            .limit(1)
        if len(single_item_in_cart_query) == 0:
            raise ItemNotFoundException("cart item")
        return {"bike_id": str(single_item_in_cart_query[0].bike_id.id)}

    @async_wrapper
    def dao_add_item_into_cart(self, user_id, bike_id):
        CartItem.create(user_id=user_id, bike_id=bike_id, created_on=datetime.now(tz=None))

    @async_wrapper
    def dao_delete_single_item_from_cart(self, user_id, bike_id):
        CartItem \
            .delete() \
            .where(CartItem.user_id == user_id and CartItem.bike_id == bike_id) \
            .execute()
