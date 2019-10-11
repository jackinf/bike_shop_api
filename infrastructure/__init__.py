from infrastructure.firebase_settings import firebase_init
from infrastructure.relational_db.seed_relational_db import seed_relational_db


def init():
    firebase_init()
    seed_relational_db(False)