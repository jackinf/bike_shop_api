from features.carts.cart_handler import CartHandler
from features.carts.sql_cart_dao import SqlCartDao


# noinspection PyUnusedLocal
class SqlBikeHandler(CartHandler, SqlCartDao):
    pass
