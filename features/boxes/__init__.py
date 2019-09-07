from aiohttp import web
from firebase_admin import db


def add(request):
    color = request.match_info.get('color', "Anonymous")
    if color is None:
        raise Exception('Error', 'color not specified')

    ref = db.reference('boxes')
    ref.push({
        'color': color,
        'width': 7,
        'height': 8,
        'length': 6
    })
    return web.json_response({"ok": True})


def update(request):
    ref = db.reference('boxes')
    box_ref = ref.child('box001')
    box_ref.update({
        'color': 'blue'
    })
    return web.json_response({"ok": True})


def search(request):
    boxes = db.reference('boxes').get()
    return web.json_response(boxes)


def register_routes(app):
    return app.add_routes([web.get('/boxes/search', search),
                           web.get('/boxes/update', update),
                           web.get('/boxes/add', add)])
