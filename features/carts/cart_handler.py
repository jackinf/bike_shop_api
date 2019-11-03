from aiohttp import web
from aiohttp_swagger import *

from constants import RequestContextKeys
from features.auth.auth_dao import AuthDao
from features.bikes.bike_dao import BikeDao
from helpers import extract_email_from_request
from .cart_dao import CartDao


# noinspection PyUnusedLocal
class CartHandler(CartDao, AuthDao, BikeDao):
    def __init__(self):
        pass

    @swagger_path("features/carts/swagger/get-cart-for-user.yaml")
    async def get_cart_items_for_user(self, request):
        user, error = await self._get_current_user(request)
        if error is not None:
            return web.json_response({"error": error}, status=400)

        bikes = await super().dao_get_items_from_cart(user.id)
        return web.json_response({"items": bikes})

    @swagger_path("features/carts/swagger/add-to-cart.yaml")
    async def add_to_cart(self, request):
        result, error = await self._extract_user_and_bike_ids_from_request(request)
        if error is not None:
            return web.json_response({"error": error}, status=400)
        user, bike = result

        result, error = await super().dao_get_single_cart_item(user.id, bike.id)
        if result is not None:
            return web.json_response({"error": "Item is already in the cart"}, status=400)

        await super().dao_add_item_into_cart(user.id, bike.id)
        return web.json_response({"ok": True})

    @swagger_path("features/carts/swagger/remove-from-cart.yaml")
    async def remove_from_cart(self, request):
        result, error = await self._extract_user_and_bike_ids_from_request(request)
        if error is not None:
            return web.json_response({"error": error}, status=400)
        user, bike = result

        result, error = await super().dao_get_single_cart_item(user.id, bike.id)
        if result is None:
            return web.json_response({"error": "Item is not in the cart"}, status=400)

        await super().dao_delete_single_item_from_cart(user.id, bike.id)
        return web.json_response({"ok": True})

    @swagger_path("features/carts/swagger/get-cart-for-current-user.yaml")
    async def get_cart_for_current_user(self, request):
        request[RequestContextKeys.email] = request[RequestContextKeys.auth_user]["email"]
        return await self.get_cart_items_for_user(request)

    @swagger_path("features/carts/swagger/add-to-cart-for-current-user.yaml")
    async def add_to_cart_for_current_user(self, request):
        request[RequestContextKeys.email] = request[RequestContextKeys.auth_user]["email"]
        return await self.add_to_cart(request)

    @swagger_path("features/carts/swagger/remove-from-cart-for-current-user.yaml")
    async def remove_from_cart_for_current_user(self, request):
        request[RequestContextKeys.email] = request[RequestContextKeys.auth_user]["email"]
        return await self.remove_from_cart(request)

    async def _extract_user_and_bike_ids_from_request(self, request):
        user, error = await self._get_current_user(request)
        if error is not None:
            return None, {"error": error}

        if "bike_id" not in request.rel_url.query:
            return None, {"error": "`bike_id` query parameter must be provided"}
        bike_id = request.rel_url.query["bike_id"]
        bike = await super().dao_get_bike(bike_id)
        if bike is None:
            return None, f"Bike with id {bike_id} was not found"
        return (user, bike), None

    async def _get_current_user(self, request):
        email = extract_email_from_request(request)
        if email is None:
            return None, "`email` query parameter must be provided"
        user = await super().dao_get_user_by_email(email)
        if user is None:
            return None, f"User with email {email} was not found"
        return user, None
