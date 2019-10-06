from datetime import datetime
from aiohttp import web
from aiohttp_swagger import *

from exceptions import ArgumentException, ItemNotFoundException
from features.bikes.bike_dao import BikeDao
from helpers import extract_search_query_parameters


# noinspection PyUnusedLocal
class BikeHandler(BikeDao):
    @swagger_path("features/bikes/swagger/search.yaml")
    async def search_bike_types(self, request):
        search_parameters = extract_search_query_parameters(request.rel_url.query)
        bike_types, total = await self.dao_search_bike_types(**search_parameters)
        return web.json_response({"items": bike_types, "total": total})

    @swagger_path("features/bikes/swagger/search.yaml")
    async def search_bikes(self, request):
        search_parameters = extract_search_query_parameters(request.rel_url.query)
        bikes, total = await self.dao_search_bikes(search_parameters)
        return web.json_response({"items": bikes, "total": total})

    async def add_bike(self, request):
        body = await request.json()
        if "bike_type_id" not in body:
            raise ArgumentException("bike_type_id")
        if "purchase_price" not in body:
            raise ArgumentException("purchase_price")

        bike_id = await self.dao_add_bike({
            "bike_type_id": body.get("bike_type_id"),
            "purchase_price": float(body.get("purchase_price")),
            "selling_price": float(body.get("purchase_price", 0)),
            "user_id": None,
            "status_key": 0,
            "created_on": datetime.now(tz=None)
        })
        return web.json_response({"ok": True, "id": bike_id})

    async def update_bike(self, request):
        bike_id = request.match_info['bike_id']
        body = await request.json()

        bike = self.dao_get_bike(bike_id)
        if bike is None:
            raise ItemNotFoundException("There is no bike with such id")

        bike.purchase_price = body.get("purchase_price")
        bike.selling_price = body.get("purchase_price")
        bike.user_id = body.get("user_id", None)
        bike.status_key = body.get("status_key", 0)
        bike.updated_on = datetime.now(tz=None)

        await self.dao_update_bike(bike)
        return web.json_response({"ok": True})

    async def remove_bike(self, request):
        bike_id = request.rel_url.query['id']
        await self.dao_remove_bike(bike_id)
        return web.json_response({"ok": True})

    async def generate_bikes(self, request):
        count = 4
        if 'count' in request.rel_url.query:
            count = int(request.rel_url.query['count'])
        await self.dao_delete_all_bikes()
        await self.dao_generate_bikes(count)
        return web.json_response({"ok": True})
