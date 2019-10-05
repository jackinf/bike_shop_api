from features.bikes.bike_handler import BikeHandler
from features.bikes.sql_bike_dao import SqlBikeDao


# noinspection PyUnusedLocal
class SqlBikeHandler(BikeHandler, SqlBikeDao):
    pass
