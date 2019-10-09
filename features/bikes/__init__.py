from aiohttp import web

from features.bikes.firebase_bike_handler import FirebaseBikeHandler
from features.bikes.sql_bike_handler import SqlBikeHandler


def register_routes(app):
    handler = SqlBikeHandler()

    bike_type_app = web.Application()
    bike_type_app.add_routes([web.get('/search', handler.search_bike_types)])
    bike_type_app.add_routes([web.get('/{bike_type_id}/bikes/search', handler.search_bikes_of_bike_type)])
    app.add_subapp('/bike-types/', bike_type_app)

    bike_app = web.Application()
    bike_app.add_routes([web.get('/search', handler.search_bikes)])
    bike_app.add_routes([web.post('/generate', handler.generate_bikes)])
    bike_app.add_routes([web.post('/add', handler.add_bike)])
    bike_app.add_routes([web.post('/update/{bike_id}', handler.update_bike)])
    bike_app.add_routes([web.delete('/remove', handler.remove_bike)])
    app.add_subapp('/bikes/', bike_app)
