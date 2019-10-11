from aiohttp import web


class MetadataHandler():
    async def get_config(self, request):
        return web.json_response({

        })