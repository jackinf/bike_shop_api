from aiohttp import web
from firebase_admin import firestore


def search(request):
    """
    Uses Cloud Firestore to query for document
    Firestore Client: https://googleapis.github.io/google-cloud-python/latest/firestore/client.html
    Quick-start for Firestore - https://firebase.google.com/docs/firestore/quickstart
    """

    db = firestore.client()
    users_ref = db.collection(u'bikes')
    docs = users_ref.stream()

    # Use lambdas to convert to normal form - https://book.pythontips.com/en/latest/map_filter.html
    bikes = list(map(lambda doc: doc.to_dict(), docs))
    return web.json_response(bikes)


def register_routes(app):
    return app.add_routes([web.get('/bikes/search', search)])
