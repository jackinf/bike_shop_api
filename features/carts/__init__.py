from aiohttp import web

from middlewares.authMiddleware import authMiddleware
from .firebase_cart_handler import FirebaseCartHandler


def register_routes(app):
    handler = FirebaseCartHandler()

    bike_app = web.Application(middlewares=[authMiddleware])
    bike_app.add_routes([web.get('', handler.get_cart_for_user)])
    bike_app.add_routes([web.post('', handler.add_to_cart)])
    bike_app.add_routes([web.delete('', handler.remove_from_cart)])
    bike_app.add_routes([web.get('/current-user', handler.get_cart_for_current_user)])
    bike_app.add_routes([web.post('/current-user', handler.add_to_cart_for_current_user)])
    bike_app.add_routes([web.delete('/current-user', handler.remove_from_cart_for_current_user)])
    app.add_subapp('/carts/', bike_app)
