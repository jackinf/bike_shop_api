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
setup_swagger(app)


if __name__ == '__main__':
    web.run_app(app, port=8082)
