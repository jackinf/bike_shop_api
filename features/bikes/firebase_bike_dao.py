import random
from datetime import datetime
from google.cloud import firestore
from google.cloud.firestore_v1 import Increment

from features.bikes.bike_dao import BikeDao
from helpers import async_wrapper, randomString


# TODO: initialize firestore client in constructor, transaction
class FirebaseBikeDao(BikeDao):
    """
    Uses Cloud Firestore to query for document
    Firestore Client: https://googleapis.github.io/google-cloud-python/latest/firestore/client.html
    Quick-start for Firestore - https://firebase.google.com/docs/firestore/quickstart
    Querying data - https://firebase.google.com/docs/firestore/query-data/get-data
    Querying data - https://cloud.google.com/firestore/docs/query-data/queries
    """

    @async_wrapper
    def dao_search_bikes(self, page, rows_per_page, order_direction, order_column, filter_keyword):
        offset = page * rows_per_page
        if order_direction == 'desc':
            firestore_order_direction = firestore.Query.DESCENDING
        else:
            firestore_order_direction = firestore.Query.ASCENDING

        db = firestore.Client()
        bikes_ref = db.collection(u'bikes')

        sort_options = {
            "title": lambda ref: ref.order_by('title', direction=firestore_order_direction),
            "price": lambda ref: ref.order_by('price', direction=firestore_order_direction),
            "stars": lambda ref: ref.order_by('stars', direction=firestore_order_direction),
            "createdOn": lambda ref: ref.order_by('createdOn', direction=firestore_order_direction),
        }

        if filter_keyword is not None:
            bikes_ref = sort_options["title"](bikes_ref)
            bikes_ref = bikes_ref \
                .where('title', '>=', filter_keyword) \
                .where('title', '<', filter_keyword + '\uf8ff')
        elif order_column in sort_options:
            bikes_ref = sort_options[order_column](bikes_ref)
        else:
            bikes_ref = sort_options["createdOn"](bikes_ref)

        stream = bikes_ref \
            .offset(offset) \
            .limit(rows_per_page) \
            .stream()

        bikes = []
        for doc in stream:
            item = doc.to_dict()
            bikes.append({
                "id": doc.id,
                "title": item['title'],
                "price": item['price'],
                "stars": item['stars'],
                "createdOn": item["createdOn"].__str__()
            })

        total = db.collection('bikes').document("metainfo").get().to_dict()["total"]
        return bikes, total

    @async_wrapper
    def get_all(self):
        docs = firestore.Client().collection(u'bikes').stream()
        bikes = list(map(lambda doc: {"id": doc.id, **doc.to_dict()}, docs))
        return bikes

    @async_wrapper
    def dao_add_bike(self, bike):
        db = firestore.Client()
        tran = db.transaction()
        doc = db.collection('bikes').document()
        doc.set(bike)
        db.collection('bikes').document("metainfo").set({"total": Increment(1)}, merge=True)
        tran.commit()

        return doc.id

    @async_wrapper
    def dao_remove_bike(self, bike_id):
        db = firestore.Client()
        tran = db.transaction()
        db.collection('bikes').document(bike_id).delete()
        db.collection('bikes').document("metainfo").set({"total": Increment(-1)}, merge=True)
        tran.commit()

    @async_wrapper
    def dao_generate_bikes(self, number):
        db = firestore.Client()
        tran = db.transaction()
        for i in range(0, number):
            db.collection('bikes').document().set({
                "title": randomString(10),
                "price": random.randint(100, 2000),
                "stars": random.choice([1, 2, 3, 4, 5]),
                "createdOn": datetime.now(tz=None)
            }, merge=True)
            db.collection('bikes').document("metainfo").set({
                "total": Increment(1)
            }, merge=True)
        tran.commit()

    @async_wrapper
    def dao_delete_all_bikes(self):
        def delete_collection(coll_ref, batch_size):
            docs = coll_ref.limit(batch_size).get()
            deleted = 0

            for doc in docs:
                print(u'Deleting doc {} => {}'.format(doc.id, doc.to_dict()))
                doc.reference.delete()
                deleted = deleted + 1

            if deleted >= batch_size:
                return delete_collection(coll_ref, batch_size)
        delete_collection(firestore.Client().collection('bikes'), 5)