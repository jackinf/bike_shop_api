from features.auth.sql_auth_dao import SqlAuthDao


class IsInRole(object):
    def __init__(self, role_name):
        self.role_name = role_name

    def __call__(self, f):
        async def wrapped_f(handler, request):
            email = request['auth_user']['email']

            print(f"Decorator arguments: Role={self.role_name}, Email={email}")

            sql_dao = SqlAuthDao()
            roles = await sql_dao.dao_get_roles_for_user(None)
            if self.role_name not in roles:
                raise Exception("User is not allowed to see this page")

            await f(handler, request)
        return wrapped_f
