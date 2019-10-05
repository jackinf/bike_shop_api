from features.bikes.bike_handler import BikeHandler
from features.bikes.firebase_bike_dao import FirebaseBikeDao


class FirebaseBikeHandler(BikeHandler, FirebaseBikeDao):
    pass
