# from google.cloud import firestore
# from google.cloud.firestore_v1 import DocumentReference
#
# from constants import CollectionName
# from decorators.async_wrapper import async_wrapper
# from .cart_dao import CartDao
#
#
# class FirebaseCartDao(CartDao):
#     @async_wrapper
#     def dao_get_single_cart(self, cart_id):
#         cart_snapshot = firestore.Client().collection(CollectionName.carts).document(cart_id).get()
#         if cart_snapshot.exists:
#             return {"cart_id": cart_snapshot.id, **cart_snapshot.to_dict()}
#         return None
#
#     @async_wrapper
#     def dao_get_single_bike(self, bike_id):
#         bike_snapshot = firestore.Client().collection(CollectionName.bikes).document(bike_id).get()
#         if bike_snapshot.exists:
#             return {"bike_id": bike_snapshot.id, **bike_snapshot.to_dict()}
#         return None
#
#     @async_wrapper
#     def dao_get_items_from_cart(self, cart_id):
#         items = []
#         stream = firestore.Client() \
#             .collection(CollectionName.carts) \
#             .document(cart_id) \
#             .collection('items') \
#             .stream()
#         for doc in stream:
#             item = doc.to_dict()
#             if 'bike' in item and isinstance(item['bike'], DocumentReference):
#                 bike_snapshot = item['bike'].get()
#                 items.append({"bike": {"bike_id": bike_snapshot.id, **bike_snapshot.to_dict()}})
#         return items
#
#     @async_wrapper
#     def dao_find_single_cart(self, email):
#         cart = None
#         stream = firestore.Client() \
#             .collection(CollectionName.carts) \
#             .where('email', '==', email) \
#             .limit(1) \
#             .stream()
#         for doc in stream:
#             cart = {"cart_id": doc.id, **doc.to_dict()}
#         return cart
#
#     @async_wrapper
#     def dao_find_single_item_in_cart(self, cart_id, bike_id):
#         item = None
#         stream = firestore.Client() \
#             .collection(CollectionName.carts) \
#             .document(cart_id) \
#             .collection('items') \
#             .where('bike_id', '==', bike_id) \
#             .limit(1) \
#             .stream()
#         for doc in stream:
#             item = {"item_id": doc.id, **doc.to_dict()}
#         return item
#
#     @async_wrapper
#     def dao_add_item_into_cart(self, cart_id, bike_id):
#         bike_ref = firestore.Client().collection(CollectionName.bikes).document(bike_id)
#         firestore.Client() \
#             .collection(CollectionName.carts)\
#             .document(cart_id)\
#             .collection('items') \
#             .document() \
#             .set({"bike": bike_ref, "bike_id": bike_id})
#
#     @async_wrapper
#     def dao_delete_single_item_from_cart(self, cart_id, item_id):
#         firestore.Client() \
#             .collection(CollectionName.carts) \
#             .document(cart_id) \
#             .collection('items') \
#             .document(item_id) \
#             .delete()
