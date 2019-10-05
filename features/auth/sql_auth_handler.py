from features.auth.auth_handler import AuthHandler
from features.auth.sql_auth_dao import SqlAuthDao


class SqlAuthHandler(AuthHandler, SqlAuthDao):
    pass
