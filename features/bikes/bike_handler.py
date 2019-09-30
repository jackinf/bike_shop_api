from datetime import datetime

from aiohttp import web
from aiohttp_swagger import *
from google.cloud import firestore


# noinspection PyUnusedLocal
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

    async def generate_bikes(self, request):
        await self._delete_all_bikes()
        db = firestore.Client()
        db.collection('bikes').document().set({
            "title": "Bike01",
            "price": 101,
            "stars": 1,
            "createdOn": datetime.now(tz=None)
        })
        db.collection('bikes').document().set({
            "title": "Bike02",
            "price": 222,
            "stars": 2,
            "createdOn": datetime.now(tz=None)
        })
        db.collection('bikes').document().set({
            "title": "Bike03",
            "price": 302,
            "stars": 4,
            "createdOn": datetime.now(tz=None)
        })
        db.collection('bikes').document().set({
            "title": "Bike04",
            "price": 402,
            "stars": 5,
            "createdOn": datetime.now(tz=None)
        })
        db.collection('bikes').document().set({
            "title": "Bike05",
            "price": 582,
            "stars": 5,
            "createdOn": datetime.now(tz=None)
        })
        db.collection('bikes').document().set({
            "title": "Bike06",
            "price": 669,
            "stars": 2,
            "createdOn": datetime.now(tz=None)
        })
        db.collection('bikes').document().set({
            "title": "Bike07",
            "price": 725,
            "stars": 4,
            "createdOn": datetime.now(tz=None)
        })
        db.collection('bikes').document().set({
            "title": "Bike08",
            "price": 850,
            "stars": 3,
            "createdOn": datetime.now(tz=None)
        })
        db.collection('bikes').document().set({
            "title": "Bike09",
            "price": 900,
            "stars": 5,
            "createdOn": datetime.now(tz=None)
        })
        db.collection('bikes').document().set({
            "title": "Bike10",
            "price": 1000,
            "stars": 4,
            "createdOn": datetime.now(tz=None)
        })
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

        bikes_ref = firestore.Client().collection(u'bikes')

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

        return web.json_response(bikes)

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
