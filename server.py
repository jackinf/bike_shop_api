from aiohttp import web
import aiohttp_swagger

from features import bikes, boxes, carts, auth, status
import config
import infrastructure

# Initialize DAL layer as well as settings required for authentication
infrastructure.init()

# Register all the routes for all the features in the application
app = web.Application()
bikes.register_routes(app)
boxes.register_routes(app)
carts.register_routes(app)
auth.register_routes(app)
status.register_routes(app)

aiohttp_swagger.setup_swagger(app)

config.enable_cors(app)

if __name__ == '__main__':
    web.run_app(app, port=8082)
