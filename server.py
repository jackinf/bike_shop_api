import aiohttp_cors
from aiohttp import web
from firebase_settings import init
from features import bikes, boxes, carts
from aiohttp_swagger import *

# Initialize the Firebase application so that we can authenticate and use database
init()

# Register all the routes for all the features in the application
app = web.Application()
bikes.register_routes(app)
boxes.register_routes(app)
carts.register_routes(app)


async def get_status(_request):
    return web.json_response({"ok": True})
app.add_routes([web.get('/status', get_status)])
setup_swagger(app)

# Configure default CORS settings.
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})

# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route)


if __name__ == '__main__':
    web.run_app(app, port=8082)
