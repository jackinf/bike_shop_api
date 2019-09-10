from google.cloud import firestore

from constants import CollectionName
from helpers import Helpers
from .cart_dao import CartDao


class FirebaseCartDao(CartDao):
    def get_single_cart(self, cart_id):
        cart_ref = firestore.Client().collection(CollectionName.carts).document(cart_id).get()
        if cart_ref.exists:
            return {"cart_id": cart_ref.id, **cart_ref.to_dict()}
        return None

    def get_single_bike(self, bike_id):
        bike_ref = firestore.Client().collection(CollectionName.bikes).document(bike_id).get()
        if bike_ref.exists:
            return {"bike_id": bike_ref.id, **bike_ref.to_dict()}
        return None

    def get_items_from_cart(self, cart_id):
        stream = firestore.Client() \
            .collection(CollectionName.carts) \
            .document(cart_id) \
            .collection('items') \
            .stream()
        return [doc_item.to_dict() for doc_item in stream]

    def find_single_cart(self, email):
        cart = None
        stream = firestore.Client() \
            .collection(CollectionName.carts) \
            .where('email', '==', email) \
            .limit(1) \
            .stream()
        for doc in stream:
            cart = {"cart_id": doc.id, **doc.to_dict()}
        return cart

    def find_single_item_in_cart(self, cart_id, bike_id):
        bike_key = Helpers.get_bike_ref_key(bike_id)
        item = None
        stream = firestore.Client() \
            .collection(CollectionName.carts) \
            .document(cart_id) \
            .collection('items') \
            .where('bike', '==', bike_key) \
            .limit(1) \
            .stream()
        for doc in stream:
            item = {"item_id": doc.id, **doc.to_dict()}
        return item

    def add_item_into_cart(self, cart_id, document):
        firestore.Client() \
            .collection(CollectionName.carts)\
            .document(cart_id)\
            .collection('items') \
            .document() \
            .set(document)

    def delete_single_item_from_cart(self, cart_id, bike_id):
        firestore.Client() \
            .collection(CollectionName.carts) \
            .document(cart_id) \
            .collection('items') \
            .document(bike_id) \
            .delete()
