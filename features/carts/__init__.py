from aiohttp import web

from .firebase_cart_handler import FirebaseCartHandler


def register_routes(app):
    handler = FirebaseCartHandler()

    # TODO: temporarily disable auth middleware
    # bike_app = web.Application(middlewares=[authMiddleware])
    bike_app = web.Application()
    bike_app.add_routes([web.get('', handler.get_cart_for_user)])
    bike_app.add_routes([web.post('', handler.add_to_cart)])
    bike_app.add_routes([web.delete('', handler.remove_from_cart)])
    app.add_subapp('/carts/', bike_app)
