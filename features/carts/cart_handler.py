from aiohttp import web
from google.cloud import firestore
from aiohttp_swagger import *
from constants import CollectionName
from helpers import Helpers


# noinspection PyUnusedLocal
class CartHandler:

    def __init__(self):
        pass

    @swagger_path("features/carts/swagger/get-cart-for-user.yaml")
    async def get_cart_for_user(self, request):
        if 'email' not in request.rel_url.query:
            return web.json_response({"error": "`email` query parameter must be provided"}, status=400)
        firestore_client = firestore.Client()
        cart_str = self._get_single_cart(firestore.Client(), request.rel_url.query['email'])

        cart = None
        for cart_ref in cart_str:
            items_str = firestore_client\
                .collection(CollectionName.carts)\
                .document(cart_ref.id)\
                .collection('items')\
                .stream()
            items = [doc_item.to_dict() for doc_item in items_str]
            cart = {"cart_id": cart_ref.id, **cart_ref.to_dict(), "bikes": items}
            break  # we need only one item

        if cart is None:
            return web.json_response({"error": "Cart not found"}, status=404)

        return web.json_response(cart)

    @swagger_path("features/carts/swagger/add-to-cart.yaml")
    async def add_to_cart(self, request):
        if 'bike_id' not in request.rel_url.query:
            return web.json_response({"error": "`bike_id` query parameter must be provided"}, status=400)
        # TODO: replace cart_id with email: use user's email to find or create a cart
        if 'cart_id' not in request.rel_url.query:
            return web.json_response({"error": "`cart_id` query parameter must be provided"}, status=400)
        bike_id = request.rel_url.query['bike_id']
        cart_id = request.rel_url.query['cart_id']

        firestore_client = firestore.Client()

        # Check if bike exists
        try:
            bike = firestore_client.collection(CollectionName.bikes).document(bike_id).get()
        except Exception as e:
            print(f'Error: {e}')
            return web.json_response({"error": "No such bike document!"}, status=400)

        # Check if cart exists
        # TODO: Find cart by email. Ff cart does not exist then create one
        try:
            cart = firestore_client.collection(CollectionName.carts).document(cart_id).get()
        except Exception as e:
            print(f'Error: {e}')
            return web.json_response({"error": "No such cart document!"}, status=400)

        # Check if an item is in the cart already
        bike_key = Helpers.get_bike_ref_key(bike_id)
        items_in_cart = self._get_items_collection_in_cart(firestore_client, cart_id)
        existing_item_result = self._find_item_in_cart(items_in_cart, bike_key)
        if len(existing_item_result) > 0:
            return web.json_response({"ok": False, "reason": "The bike is already in the cart"}, status=200)

        # Add a bike reference into cart
        items_in_cart.document().set({"bike": bike_key})

        return web.json_response({"ok": True})

    @swagger_path("features/carts/swagger/remove-from-cart.yaml")
    async def remove_from_cart(self, request):
        if 'bike_id' not in request.rel_url.query:
            return web.json_response({"error": "`bike_id` query parameter must be provided"}, status=400)
        # TODO: replace cart_id with email: use user's email to find or create a cart
        if 'cart_id' not in request.rel_url.query:
            return web.json_response({"error": "`cart_id` query parameter must be provided"}, status=400)
        bike_id = request.rel_url.query['bike_id']
        cart_id = request.rel_url.query['cart_id']

        firestore_client = firestore.Client()

        # Check if cart exists
        # TODO: Find cart by email. Ff cart does not exist then create one
        try:
            cart = firestore_client.collection(CollectionName.carts).document(cart_id).get()
        except Exception as e:
            print(f'Error: {e}')
            return web.json_response({"error": "No such cart document!"}, status=400)

        # Check if an item is in the cart
        items_in_cart = self._get_items_collection_in_cart(firestore_client, cart_id)
        existing_item_result = self._find_item_in_cart(items_in_cart, Helpers.get_bike_ref_key(bike_id))
        if len(existing_item_result) == 0:
            return web.json_response({"ok": False, "reason": "There is no such bike in the cart"}, status=200)

        bike_id = existing_item_result[0]
        items_in_cart.document(bike_id).delete()

        return web.json_response({"ok": True})

    @staticmethod
    def _get_single_cart(firestore_client, email):
        return firestore_client \
            .collection(CollectionName.carts) \
            .where('email', '==', email) \
            .limit(1) \
            .stream()

    @staticmethod
    def _find_item_in_cart(items_in_cart, bike_key):
        existing_item_str = items_in_cart\
            .where('bike', '==', bike_key)\
            .limit(1)\
            .stream()
        return [item.id for item in existing_item_str]

    @staticmethod
    def _get_items_collection_in_cart(firestore_client, cart_id):
        return firestore_client\
            .collection(CollectionName.carts)\
            .document(cart_id)\
            .collection('items')