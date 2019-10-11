from aiohttp import web


def register_routes(app):
    async def get_status(_request):
        return web.json_response({"ok": True})

    app.add_routes([web.get('/status', get_status)])
