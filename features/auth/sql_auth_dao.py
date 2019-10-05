from features.auth.auth_dao import AuthDao
from helpers import async_wrapper


class SqlAuthDao(AuthDao):
    @async_wrapper
    def dao_create_user(self, **kwargs):
        raise NotImplementedError()

    @async_wrapper
    def dao_get_users(self):
        raise NotImplementedError()

    @async_wrapper
    def dao_get_roles_for_user(self, user_id):
        raise NotImplementedError()

    @async_wrapper
    def dao_get_user_by_email(self, email):
        raise NotImplementedError()
