from aiohttp import web

from features.auth.sql_auth_handler import SqlAuthHandler
from middlewares.authMiddleware import authMiddleware


def register_routes(app):
    handler = SqlAuthHandler()

    bike_app = web.Application(middlewares=[authMiddleware])
    bike_app.add_routes([web.get('/init', handler.initialize_current_user)])
    bike_app.add_routes([web.get('/users', handler.get_users)])
    bike_app.add_routes([web.get('/get-roles', handler.get_roles_for_current_user)])
    app.add_subapp('/auth/', bike_app)
