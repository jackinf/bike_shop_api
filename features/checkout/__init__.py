from aiohttp import web

from features.auth.sql_auth_dao import SqlAuthDao
from features.carts.sql_cart_dao import SqlCartDao
from features.checkout.checkout_handler import CheckoutHandler
from middlewares.authMiddleware import authMiddleware


class SqlCheckoutHandler(CheckoutHandler, SqlCartDao, SqlAuthDao):
    pass


def register_routes(app):
    handler = SqlCheckoutHandler()

    checkout_app = web.Application(middlewares=[authMiddleware])
    checkout_app.add_routes([web.get('/summary', handler.handle_get_summary)])
    checkout_app.add_routes([web.get('/finalize-order', handler.handle_finalize_order)])
    app.add_subapp('/checkout/', checkout_app)