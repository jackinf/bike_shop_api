from aiohttp import web
from .bike_handler import BikeHandler


def register_routes(app):
    handler = BikeHandler()

    bike_app = web.Application()
    bike_app.add_routes([web.get('/get-all', handler.get_all)])
    bike_app.add_routes([web.get('/search', handler.handle_search)])
    bike_app.add_routes([web.post('/generate', handler.generate_bikes)])
    bike_app.add_routes([web.post('/add', handler.add_bike)])
    bike_app.add_routes([web.delete('/remove', handler.remove_bike)])
    app.add_subapp('/bikes/', bike_app)
