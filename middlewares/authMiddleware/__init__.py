from aiohttp import web
from aiohttp.web_exceptions import HTTPForbidden
from firebase_admin import auth


@web.middleware
async def authMiddleware(request, handler):
    authorization_header = request.headers.get('AUTHORIZATION')
    if authorization_header is None:
        raise HTTPForbidden()
    token = authorization_header.split(' ')[-1]
    try:
        auth.verify_id_token(token)
        response = await handler(request)
        return response
    except ValueError as e:
        print(e)
        raise HTTPForbidden()