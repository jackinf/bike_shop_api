from datetime import datetime

from constants import UserRoleName
from infrastructure.relational_db import db
from infrastructure.relational_db.models import User, UserRole, Role
from decorators.async_wrapper import async_wrapper
from features.auth.auth_dao import AuthDao


class SqlAuthDao(AuthDao):
    def __enter__(self):
        db.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        db.close()

    @async_wrapper
    def dao_create_user(self, **kwargs):
        user = User.create(email=kwargs.get('email'), name=kwargs.get('name', None), created_on=datetime.now(tz=None))
        role = Role.select().where(Role.name == UserRoleName.user).limit(1)[0]
        if len(UserRole.select().where(UserRole.user_id == user.id and UserRole.role_id == role.id).limit(1)) == 0:
            UserRole.create(user_id=user.id, role_id=role.id, created_on=datetime.now(tz=None))

    @async_wrapper
    def dao_get_users(self):
        results = []
        for item in UserRole.select():
            results.append({"role": item.role_id.name, "email": item.user_id.email})
        return results

    @async_wrapper
    def dao_get_user_by_email(self, email):
        roles = [x.role_id.name for x in UserRole.select().join(User).where(UserRole.user_id.email == email)]
        return roles
