from aiohttp import web


def register_routes(app):
    handler = MetadataHandler()

    bike_app = web.Application()
    bike_app.add_routes([web.get('/config', handler.get_config)])
    app.add_subapp('/metadata/', bike_app)
