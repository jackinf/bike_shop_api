from aiohttp import web
from firebase_admin import firestore
from aiohttp_swagger import *


@swagger_path("features/bikes/swagger/search.yaml")
async def search(request):
    """
    Uses Cloud Firestore to query for document
    Firestore Client: https://googleapis.github.io/google-cloud-python/latest/firestore/client.html
    Quick-start for Firestore - https://firebase.google.com/docs/firestore/quickstart
    Querying data - https://firebase.google.com/docs/firestore/query-data/get-data
    Querying data - https://cloud.google.com/firestore/docs/query-data/queries
    """

    db = firestore.client()
    users_ref = db.collection(u'bikes')
    docs = users_ref.stream()

    # Use lambdas to convert to normal form - https://book.pythontips.com/en/latest/map_filter.html
    bikes = list(map(lambda doc: doc.to_dict(), docs))
    return web.json_response(bikes)


def register_routes(app):
    bike_app = web.Application()
    bike_app.add_routes([web.get('/search', search)])
    app.add_subapp('/bikes/', bike_app)
