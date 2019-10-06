from pprint import pprint

from dal.relational_db import db
from dal.relational_db.models import UserRole, User

db.connect()

query_01 = UserRole.select()
for item in query_01:
    pprint(f'Role: {item.role_id.name}; Email: {item.user_id.email}')

query_02 = User.select().join(UserRole)
for item in query_02:
    for user_role in item.user_roles:
        pprint(user_role.role_id.name)

query_03 = UserRole.select().join(User).where(UserRole.user_id.email == "zeka.rum@gmail.com")
roles = []
for result in query_03:
    roles.append(result.role_id.name)
pprint(roles)

roles_1 = [x.role_id.name for x in UserRole.select().join(User).where(UserRole.user_id.email == "zeka.rum@gmail.com")]
pprint(roles_1)

db.close()
