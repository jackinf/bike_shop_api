import random
from datetime import datetime
from aiohttp import web
from aiohttp_swagger import *

from features.bikes.bike_dao import BikeDao
from helpers import randomString


# noinspection PyUnusedLocal
class BikeHandler(BikeDao):
    async def get_all(self, request):
        bikes = await self.dao_get_all_bikes()
        return web.json_response(bikes)

    async def add_bike(self, request):
        # bike_id = await self.dao_add_bike({
        #     "title": randomString(10),
        #     "price": random.randint(100, 2000),
        #     "stars": random.choice([1, 2, 3, 4, 5]),
        #     "createdOn": datetime.now(tz=None)
        # })
        bike_id = await self.dao_add_bike({
            "purchase_price": random.randint(100, 2000),
            "selling_price": None,
            "user_id": None,
            "status_key": 0,
            "createdOn": datetime.now(tz=None)
        })
        return web.json_response({"ok": True, "id": bike_id})

    async def remove_bike(self, request):
        bike_id = request.rel_url.query['id']
        await self.dao_remove_bike(bike_id)
        return web.json_response({"ok": True})

    async def generate_bikes(self, request):
        await self.dao_delete_all_bikes()
        await self.dao_generate_bikes(4)
        return web.json_response({"ok": True})

    @swagger_path("features/bikes/swagger/search.yaml")
    async def handle_search(self, request):
        page = 0
        rows_per_page = 10
        order_direction = 'asc'
        order_column = 'createdOn'
        filter_keyword = None

        if 'rows_per_page' in request.rel_url.query:
            rows_per_page = int(request.rel_url.query['rows_per_page'])
        if 'page' in request.rel_url.query:
            page = int(request.rel_url.query['page'])
        if 'order_column' in request.rel_url.query:
            order_column = request.rel_url.query['order_column']
        if 'order_direction' in request.rel_url.query:
            order_direction = request.rel_url.query['order_direction']
        if 'filter_keyword' in request.rel_url.query:
            filter_keyword = request.rel_url.query['filter_keyword']

        print("=========")
        print(f"rows_per_page: {rows_per_page}; "
              f"filter_keyword: {filter_keyword}; "
              f"order_direction: {order_direction}; "
              f"order_column: {order_column}")

        bikes, total = await self.dao_search_bikes(page, rows_per_page, order_direction, order_column, filter_keyword)
        return web.json_response({"items": bikes, "total": total})
