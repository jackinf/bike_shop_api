import random
from datetime import datetime
from google.cloud.firestore_v1 import Increment

from aiohttp import web
from aiohttp_swagger import *
from google.cloud import firestore


# noinspection PyUnusedLocal
from helpers import randomString


class BikeHandler:
    """
    Uses Cloud Firestore to query for document
    Firestore Client: https://googleapis.github.io/google-cloud-python/latest/firestore/client.html
    Quick-start for Firestore - https://firebase.google.com/docs/firestore/quickstart
    Querying data - https://firebase.google.com/docs/firestore/query-data/get-data
    Querying data - https://cloud.google.com/firestore/docs/query-data/queries
    """

    def __init__(self):
        pass

    async def get_all(self, request):
        db = firestore.Client()
        users_ref = db.collection(u'bikes')
        docs = users_ref.stream()

        # Use lambdas to convert to normal form - https://book.pythontips.com/en/latest/map_filter.html
        bikes = list(map(lambda doc: {"id": doc.id, **doc.to_dict()}, docs))

        return web.json_response(bikes)

    async def add_bike(self, request):
        db = firestore.Client()

        tran = db.transaction()
        doc = db.collection('bikes').document()
        doc.set({
            "title": randomString(10),
            "price": random.randint(100, 2000),
            "stars": random.choice([1, 2, 3, 4, 5]),
            "createdOn": datetime.now(tz=None)
        })
        db.collection('bikes').document("metainfo").set({"total": Increment(1)}, merge=True)

        tran.commit()
        return web.json_response({"ok": True, "id": doc.id})

    async def remove_bike(self, request):
        db = firestore.Client()
        tran = db.transaction()
        db.collection('bikes').document(request.rel_url.query['id']).delete()
        db.collection('bikes').document("metainfo").set({"total": Increment(-1)}, merge=True)
        tran.commit()
        return web.json_response({"ok": True})

    async def generate_bikes(self, request):
        await self._delete_all_bikes()
        db = firestore.Client()
        tran = db.transaction()
        for i in range(0, 4):
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
        return web.json_response({"ok": True})

    @swagger_path("features/bikes/swagger/search.yaml")
    async def handle_search(self, request):
        rows_per_page = 10
        page = 0
        order_direction = 'asc'
        order_column = 'createdOn'
        filter_keyword = None

        if 'rows_per_page' in request.rel_url.query:
            rows_per_page = int(request.rel_url.query['rows_per_page'])
        if 'page' in request.rel_url.query:
            page = int(request.rel_url.query['page'])
        if 'order_column' in request.rel_url.query:
            order_column = request.rel_url.query['order_column']
        if 'order_direction' in request.rel_url.query:
            order_direction = request.rel_url.query['order_direction']
        if 'filter_keyword' in request.rel_url.query:
            filter_keyword = request.rel_url.query['filter_keyword']

        print("=========")
        print(f"rows_per_page: {rows_per_page}; "
              f"filter_keyword: {filter_keyword}; "
              f"order_direction: {order_direction}; "
              f"order_column: {order_column}")

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
            bikes_ref = bikes_ref\
                .where('title', '>=', filter_keyword)\
                .where('title', '<', filter_keyword+'\uf8ff')
        elif order_column in sort_options:
            bikes_ref = sort_options[order_column](bikes_ref)
        else:
            bikes_ref = sort_options["createdOn"](bikes_ref)

        stream = bikes_ref\
            .offset(offset)\
            .limit(rows_per_page)\
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

        print(f'Bikes: {bikes}')

        total = db.collection('bikes').document("metainfo").get().to_dict()["total"]
        return web.json_response({"items": bikes, "total": total})

    async def _delete_all_bikes(self):
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
