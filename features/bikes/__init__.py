from aiohttp import web
from middlewares.authMiddleware import authMiddleware
from .bike_handler import BikeHandler


def register_routes(app):
    handler = BikeHandler()

    bike_app = web.Application(middlewares=[authMiddleware])
    bike_app.add_routes([web.get('/search', handler.handle_search)])
    app.add_subapp('/bikes/', bike_app)
