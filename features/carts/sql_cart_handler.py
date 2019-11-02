from features.auth.sql_auth_dao import SqlAuthDao
from features.bikes.sql_bike_dao import SqlBikeDao
from features.carts.cart_handler import CartHandler
from features.carts.sql_cart_dao import SqlCartDao


# noinspection PyUnusedLocal
class SqlCartHandler(CartHandler, SqlCartDao, SqlAuthDao, SqlBikeDao):
    pass
