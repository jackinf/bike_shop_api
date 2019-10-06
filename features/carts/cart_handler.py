from aiohttp import web
from aiohttp_swagger import *

from constants import RequestContextKeys
from .cart_dao import CartDao


def _extract_email(request):
    email = None
    if RequestContextKeys.email in request:
        email = request[RequestContextKeys.email]
    elif 'email' in request.rel_url.query:
        email = request.rel_url.query["email"]
    return email


# noinspection PyUnusedLocal
class CartHandler(CartDao):
    def __init__(self):
        pass

    @swagger_path("features/carts/swagger/get-cart-for-user.yaml")
    async def get_cart_for_user(self, request):
        email = _extract_email(request)
        if email is None:
            return web.json_response({"error": "`email` query parameter must be provided"}, status=400)

        cart = await super().find_single_cart(email)
        if cart is None:
            return web.json_response({"error": "Cart not found"}, status=404)

        items = await super().get_items_from_cart(cart["cart_id"])
        return web.json_response({**cart, "items": items})

    @swagger_path("features/carts/swagger/add-to-cart.yaml")
    async def add_to_cart(self, request):
        (result, error) = await self._parse_inputs_and_try_to_find_bike_in_cart(request)
        if error is not None:
            return web.json_response(error, status=400)
        if result is None:
            return web.json_response("Unexpected behaviour", status=500)
        (item, cart, bike) = result
        if item is not None:
            return web.json_response({"ok": False, "reason": "There is already a bike in the cart"}, status=200)

        await super().add_item_into_cart(cart["cart_id"], bike["bike_id"])

        return web.json_response({"ok": True})

    @swagger_path("features/carts/swagger/remove-from-cart.yaml")
    async def remove_from_cart(self, request):
        (result, error) = await self._parse_inputs_and_try_to_find_bike_in_cart(request)
        if error is not None:
            return web.json_response(error, status=400)
        if result is None:
            return web.json_response("Unexpected behaviour", status=500)
        (item, cart, bike) = result
        if item is None:
            return web.json_response({"ok": False, "reason": "There is no such bike in the cart"}, status=200)

        await super().delete_single_item_from_cart(cart["cart_id"], item["item_id"])

        return web.json_response({"ok": True})

    @swagger_path("features/carts/swagger/get-cart-for-current-user.yaml")
    async def get_cart_for_current_user(self, request):
        request[RequestContextKeys.email] = request[RequestContextKeys.auth_user]["email"]
        return await self.get_cart_for_user(request)

    @swagger_path("features/carts/swagger/add-to-cart-for-current-user.yaml")
    async def add_to_cart_for_current_user(self, request):
        request[RequestContextKeys.email] = request[RequestContextKeys.auth_user]["email"]
        return await self.add_to_cart(request)

    @swagger_path("features/carts/swagger/remove-from-cart-for-current-user.yaml")
    async def remove_from_cart_for_current_user(self, request):
        request[RequestContextKeys.email] = request[RequestContextKeys.auth_user]["email"]
        return await self.remove_from_cart(request)

    async def _parse_inputs_and_try_to_find_bike_in_cart(self, request):
        """
        Operations, that are being executed
        1. Tries to get bike_id as a query parameter
        2. Tries to get email either from request context or as a query parameter
        3. Tries to get a bike obj from DB
        4. Tries to get a cart obj from DB
        5. Tries to find a reference obj (the bike) in a cart
        :param request:
        :return: ((CartItem, Cart, Bike), ErrorPayload)
        """

        if "bike_id" not in request.rel_url.query:
            return None, {"error": "`bike_id` query parameter must be provided"}

        email = _extract_email(request)
        if email is None:
            return None, {"error": "`email` query parameter must be provided"}

        bike_id = request.rel_url.query["bike_id"]

        # Check if bike exists
        bike = await super().get_single_bike(bike_id)
        if bike is None:
            return None, {"error": "No such bike document!"}

        # Check if cart exists.
        cart = await super().find_single_cart(email)
        if cart is None:
            return None, {"error": "No such cart document!"}

        # Check if an item is in the cart
        item = await super().find_single_item_in_cart(cart["cart_id"], bike_id)
        return (item, cart, bike), None
