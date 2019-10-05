from aiohttp import web

from decorators.is_in_role import IsInRole
from features.auth.auth_dao import AuthDao


class AuthHandler(AuthDao):
    async def initialize_current_user(self, request):
        email = request['auth_user']["email"]
        user = await self.dao_get_user_by_email(email)
        if user is None:
            await self.dao_create_user(email=email)
        return web.json_response({"ok": True})

    @IsInRole("admin")
    async def get_users(self, request):
        users = await self.dao_get_users()
        return web.json_response({"users": users})

    async def get_roles_for_current_user(self, request):
        email = request['auth_user']["email"]
        user = await self.dao_get_user_by_email(email)
        return web.json_response({"user": user})
