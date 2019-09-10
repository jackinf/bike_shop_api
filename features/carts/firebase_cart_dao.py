import asyncio
import concurrent.futures
from google.cloud import firestore

from constants import CollectionName
from helpers import Helpers
from .cart_dao import CartDao

executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)


class FirebaseCartDao(CartDao):
    async def get_single_cart(self, cart_id):
        cart_ref_query = firestore.Client().collection(CollectionName.carts).document(cart_id)
        cart_ref = await asyncio.get_running_loop().run_in_executor(executor, cart_ref_query.get)
        if cart_ref.exists:
            return {"cart_id": cart_ref.id, **cart_ref.to_dict()}
        return None

    async def get_single_bike(self, bike_id):
        bike_ref_query = firestore.Client().collection(CollectionName.bikes).document(bike_id)
        bike_ref = await asyncio.get_running_loop().run_in_executor(executor, bike_ref_query.get)
        if bike_ref.exists:
            return {"bike_id": bike_ref.id, **bike_ref.to_dict()}
        return None

    async def get_items_from_cart(self, cart_id):
        query = firestore.Client() \
            .collection(CollectionName.carts) \
            .document(cart_id) \
            .collection('items')
        stream = await asyncio.get_running_loop().run_in_executor(executor, query.stream)
        return [doc_item.to_dict() for doc_item in stream]

    async def find_single_cart(self, email):
        cart = None
        query = firestore.Client() \
            .collection(CollectionName.carts) \
            .where('email', '==', email) \
            .limit(1)
        stream = await asyncio.get_running_loop().run_in_executor(executor, query.stream)
        for doc in stream:
            cart = {"cart_id": doc.id, **doc.to_dict()}
        return cart

    async def find_single_item_in_cart(self, cart_id, bike_id):
        bike_key = Helpers.get_bike_ref_key(bike_id)
        item = None
        query = firestore.Client() \
            .collection(CollectionName.carts) \
            .document(cart_id) \
            .collection('items') \
            .where('bike', '==', bike_key) \
            .limit(1)
        stream = await asyncio.get_running_loop().run_in_executor(executor, query.stream)
        for doc in stream:
            item = {"item_id": doc.id, **doc.to_dict()}
        return item

    async def add_item_into_cart(self, cart_id, document):
        doc = firestore.Client() \
            .collection(CollectionName.carts)\
            .document(cart_id)\
            .collection('items') \
            .document()

        def add_operation():
            doc.set(document)

        await asyncio.get_running_loop().run_in_executor(executor, add_operation)

    async def delete_single_item_from_cart(self, cart_id, bike_id):
        doc = firestore.Client() \
            .collection(CollectionName.carts) \
            .document(cart_id) \
            .collection('items') \
            .document(bike_id)
        await asyncio.get_running_loop().run_in_executor(executor, doc.delete)
