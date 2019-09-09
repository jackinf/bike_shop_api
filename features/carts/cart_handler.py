from aiohttp import web
from google.cloud import firestore
from aiohttp_swagger import *


# noinspection PyUnusedLocal
class CartHandler:

    def __init__(self):
        pass

    @swagger_path("features/carts/swagger/get-cart-for-user.yaml")
    async def get_cart_for_user(self, request):
        print(f'Request: {request}')
        # TODO: pass an email as a request in middleware
        if 'email' not in request.rel_url.query:
            return web.json_response({"error": "`email` query parameter must be provided"}, status=400)
        email = request.rel_url.query['email']

        docs = firestore.Client()\
            .collection(u'carts')\
            .where('email', '==', email)\
            .limit(1) \
            .stream()

        # Use lambdas to convert to normal form - https://book.pythontips.com/en/latest/map_filter.html
        carts = list(map(lambda doc: {"id": doc.id, **doc.to_dict()}, docs))
        if len(carts) == 0:
            return web.json_response({"error": "Cart not found"}, status=404)

        cart = carts[0]
        return web.json_response(cart)

    @swagger_path("features/carts/swagger/add-to-cart.yaml")
    async def add_to_cart(self, request):
        if 'bike_id' not in request.rel_url.query:
            return web.json_response({"error": "`bike_id` query parameter must be provided"}, status=400)
        if 'cart_id' not in request.rel_url.query:
            return web.json_response({"error": "`cart_id` query parameter must be provided"}, status=400)
        bike_id = request.rel_url.query['bike_id']
        # TODO: use user's email to find or create a cart
        cart_id = request.rel_url.query['cart_id']

        firestore_client = firestore.Client()

        # Check if bike exists
        try:
            bike = firestore_client.collection('bikes').document(bike_id).get()
            print(u'Bike data: {}'.format(bike.to_dict()))
        except Exception as e:
            print(f'Error: {e}')
            raise Exception('No such bike document! ')

        # Check if cart exists
        # TODO: if cart does not exist then create one
        try:
            cart = firestore_client.collection('carts').document(cart_id).get()
            print(u'Cart data: {}'.format(cart.to_dict()))
        except Exception as e:
            print(f'Error: {e}')
            raise Exception('No such cart document! ')

        # TODO: check if an item is in the cart already

        # Add a bike into a cart
        firestore_client\
            .collection('carts')\
            .document(cart_id)\
            .collection('items')\
            .document()\
            .set(bike_id)

        return web.json_response({"ok": True})

    @swagger_path("features/carts/swagger/remove-from-cart.yaml")
    async def remove_from_cart(self, request):
        bike_id = request.match_info.get('bike-id')
        # TODO: use user's email to find or create a cart
        cart_id = request.match_info.get('cart-id')
        if bike_id is None:
            raise Exception("Bike Id has not been provided")
        if cart_id is None:
            raise Exception("Cart Id has not been provided")

        # TODO: Check if cart exists
        # TODO: Check if bike exists in cart

        firestore.Client()\
            .collection('carts')\
            .document(cart_id)\
            .collection('items')\
            .document(bike_id)\
            .delete()

        return web.json_response({"ok": True})