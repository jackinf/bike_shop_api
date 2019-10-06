from aiohttp import web

from features.bikes.firebase_bike_handler import FirebaseBikeHandler
from features.bikes.sql_bike_handler import SqlBikeHandler


def register_routes(app):
    handler = SqlBikeHandler()

    bike_app = web.Application()
    bike_app.add_routes([web.get('/search/bike-types', handler.search_bike_types)])
    bike_app.add_routes([web.get('/search/{bike_type_id}', handler.search_bikes)])
    bike_app.add_routes([web.post('/generate', handler.generate_bikes)])
    bike_app.add_routes([web.post('/add', handler.add_bike)])
    bike_app.add_routes([web.post('/update/{bike_id}', handler.update_bike)])
    bike_app.add_routes([web.delete('/remove', handler.remove_bike)])
    app.add_subapp('/bikes/', bike_app)
