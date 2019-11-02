from pprint import pprint

from infrastructure.relational_db import db
from infrastructure.relational_db.models import User

db.connect()
user = User.select().where(User.email == "zeka.rum@gmail.com").limit(1)[0]
pprint(user)
db.close()