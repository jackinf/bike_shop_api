from constants import RequestContextKeys
from exceptions import NotInRoleException
from features.auth.sql_auth_dao import SqlAuthDao


class IsInRole(object):
    def __init__(self, role_name):
        self.role_name = role_name

    def __call__(self, next_handler):
        async def wrapper(handler, request):
            email = request[RequestContextKeys.auth_user]['email']

            print(f"Decorator arguments: Role={self.role_name}, Email={email}")

            sql_dao = SqlAuthDao()
            roles = await sql_dao.dao_get_user_by_email(email)
            if self.role_name not in roles:
                raise NotInRoleException("User is not allowed to see this page")

            await next_handler(handler, request)
        return wrapper
