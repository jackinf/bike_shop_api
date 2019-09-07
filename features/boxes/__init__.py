from aiohttp import web
from .box_handler import BoxHandler


def register_routes(app):
    handler = BoxHandler()

    box_app = web.Application()
    box_app.add_routes([
        web.get('/search', handler.handle_search),
        web.put('/update', handler.handle_update),
        web.post('/add', handler.handle_add)
    ])
    app.add_subapp('/boxes/', box_app)
