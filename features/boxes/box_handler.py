from aiohttp import web
from firebase_admin import db
from aiohttp_swagger import *


# noinspection PyUnusedLocal
class BoxHandler:
    def __init__(self):
        pass

    @swagger_path("features/boxes/swagger/add.yaml")
    async def handle_add(self, request):
        color = request.match_info.get('color', "Green")
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

    @swagger_path("features/boxes/swagger/update.yaml")
    async def handle_update(self, request):
        ref = db.reference('boxes')
        box_ref = ref.child('box001')
        box_ref.update({
            'color': 'blue'
        })
        return web.json_response({"ok": True})

    @swagger_path("features/boxes/swagger/search.yaml")
    async def handle_search(self, request):
        boxes = db.reference('boxes').get()
        return web.json_response(boxes)