import stripe
import os
from aiohttp import web

from features.auth.sql_auth_dao import SqlAuthDao
from features.carts.sql_cart_dao import SqlCartDao
from features.payments.payment_handler import PaymentHandler
from middlewares.authMiddleware import authMiddleware


class SqlPaymentHandler(PaymentHandler, SqlCartDao, SqlAuthDao):
    pass


def register_routes(app):
    stripe_api_key = os.environ['BIKESHOP_STRIPE_SECRET']
    if stripe_api_key is None:
        raise Exception(f"Stripe API key is not defined")

    stripe.api_key = stripe_api_key

    handler = SqlPaymentHandler()

    payments_app = web.Application(middlewares=[authMiddleware])
    payments_app.add_routes([web.post('/start-session', handler.handle_create_payment_indent)])
    payments_app.add_routes([web.post('/start-standalone-session', handler.handle_create_standalone_checkout_session)])
    app.add_subapp('/payments/', payments_app)
