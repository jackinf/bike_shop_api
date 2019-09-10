from abc import ABC
from aiohttp import web
from aiohttp_swagger import *

from helpers import Helpers
from .cart_dao import CartDao


# noinspection PyUnusedLocal
class CartHandler(CartDao, ABC):

    def __init__(self):
        pass

    @swagger_path("features/carts/swagger/get-cart-for-user.yaml")
    async def get_cart_for_user(self, request):
        if 'email' not in request.rel_url.query:
            return web.json_response({"error": "`email` query parameter must be provided"}, status=400)

        cart = super().find_single_cart(request.rel_url.query["email"])
        if cart is None:
            return web.json_response({"error": "Cart not found"}, status=404)

        items = super().get_items_from_cart(cart["cart_id"])
        return web.json_response({**cart, "bikes": items})

    @swagger_path("features/carts/swagger/add-to-cart.yaml")
    async def add_to_cart(self, request):
        if "bike_id" not in request.rel_url.query:
            return web.json_response({"error": "`bike_id` query parameter must be provided"}, status=400)
        # TODO: replace cart_id with email: use user's email to find or create a cart
        if "cart_id" not in request.rel_url.query:
            return web.json_response({"error": "`cart_id` query parameter must be provided"}, status=400)
        bike_id = request.rel_url.query["bike_id"]
        cart_id = request.rel_url.query["cart_id"]

        # Check if bike exists
        bike = super().get_single_bike(bike_id)
        if bike is None:
            return web.json_response({"error": "No such bike document!"}, status=400)

        # Check if cart exists. TODO: Find cart by email. Ff cart does not exist then create one
        cart = super().get_single_cart(cart_id)
        if cart is None:
            return web.json_response({"error": "No such cart document!"}, status=400)

        # Check if an item is in the cart already
        item = super().find_single_item_in_cart(cart_id, bike_id)
        if item is not None:
            return web.json_response({"ok": False, "reason": "There is already a bike in the cart"}, status=200)

        super().add_item_into_cart(cart_id, {"bike": Helpers.get_bike_ref_key(bike_id)})

        return web.json_response({"ok": True})

    @swagger_path("features/carts/swagger/remove-from-cart.yaml")
    async def remove_from_cart(self, request):
        if "bike_id" not in request.rel_url.query:
            return web.json_response({"error": "`bike_id` query parameter must be provided"}, status=400)
        # TODO: replace cart_id with email: use user's email to find or create a cart
        if "cart_id" not in request.rel_url.query:
            return web.json_response({"error": "`cart_id` query parameter must be provided"}, status=400)
        bike_id = request.rel_url.query["bike_id"]
        cart_id = request.rel_url.query["cart_id"]

        # Check if bike exists
        bike = super().get_single_bike(bike_id)
        if bike is None:
            return web.json_response({"error": "No such bike document!"}, status=400)

        # Check if cart exists. TODO: Find cart by email. Ff cart does not exist then create one
        cart = super().get_single_cart(cart_id)
        if cart is None:
            return web.json_response({"error": "No such cart document!"}, status=400)

        # Check if an item is in the cart
        item = super().find_single_item_in_cart(cart_id, bike_id)
        if item is None:
            return web.json_response({"ok": False, "reason": "There is no such bike in the cart"}, status=200)

        super().delete_single_item_from_cart(cart_id, item["item_id"])

        return web.json_response({"ok": True})
