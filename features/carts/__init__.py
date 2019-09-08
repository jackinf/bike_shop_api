from aiohttp import web
from middlewares.authMiddleware import authMiddleware
from .cart_handler import CartHandler


def register_routes(app):
    handler = CartHandler()

    bike_app = web.Application(middlewares=[authMiddleware])
    bike_app.add_routes([web.get('', handler.get_cart_for_user)])
    bike_app.add_routes([web.post('', handler.add_to_cart)])
    bike_app.add_routes([web.delete('', handler.remove_from_cart)])
    app.add_subapp('/carts/', bike_app)
