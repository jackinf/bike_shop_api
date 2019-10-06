from aiohttp import web
from aiohttp.web_exceptions import HTTPForbidden
from firebase_admin import auth

from constants import HeaderKeys, RequestContextKeys
from exceptions import NotInRoleException


@web.middleware
async def authMiddleware(request, handler):
    authorization_header = request.headers.get(HeaderKeys.authorization)
    if authorization_header is None:
        raise HTTPForbidden()
    token = authorization_header.split(' ')[-1]
    try:
        request[RequestContextKeys.auth_user] = auth.verify_id_token(token)
        response = await handler(request)
        return response
    except NotInRoleException as e:
        print(e)
        raise HTTPForbidden()
    except ValueError as e:
        print(e)
        raise HTTPForbidden()
