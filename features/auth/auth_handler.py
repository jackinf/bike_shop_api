from aiohttp import web

from features.auth.auth_dao import AuthDao
from helpers import async_wrapper


class AuthHandler(AuthDao):
    @async_wrapper
    def initialize_current_user(self, request):
        email = request['auth_user']["email"]
        user = await self.dao_get_user_by_email(email)
        if user is None:
            await self.dao_create_user(email=email)
        return web.json_response({"ok": True})

    @async_wrapper
    def get_users(self, request):
        users = await self.dao_get_users()
        return web.json_response({"users": users})

    @async_wrapper
    def get_roles_for_current_user(self, request):
        email = request['auth_user']["email"]
        user = await self.dao_get_user_by_email(email)
        return web.json_response({"user": user})
