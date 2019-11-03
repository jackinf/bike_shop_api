from aiohttp import web
from aiohttp.hdrs import METH_OPTIONS
from aiohttp.web_exceptions import HTTPForbidden
from firebase_admin import auth

from constants import HeaderKeys, RequestContextKeys
from exceptions import NotInRoleException


@web.middleware
async def authMiddleware(request, handler):
    # This handles preflight CORS requests
    if request.method == METH_OPTIONS:
        return await handler(request)

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


@web.middleware
async def optionalAuthMiddleware(request, handler):
    authorization_header = request.headers.get(HeaderKeys.authorization)
    if authorization_header is None:
        return await handler(request)
    try:
        token = authorization_header.split(' ')[-1]
        auth_user = auth.verify_id_token(token)
        email = auth_user["email"]
        request[RequestContextKeys.auth_user] = auth_user
        request[RequestContextKeys.email] = email
    except:
        pass
    return await handler(request)
