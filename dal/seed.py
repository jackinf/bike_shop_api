import datetime

from dal.relational_db import db
from dal.relational_db.models import Role, BikeStatus, BikeType


def seed_relational_db():
    db.connect()

    def check_or_create_role(name):
        if len(Role.select().where(Role.name == name).limit(1)) == 0:
            Role.create(name=name)

    check_or_create_role("admin")
    check_or_create_role("user")
    check_or_create_role("guest")

    def check_or_create_bike_status(the_key, value):
        if len(BikeStatus.select().where(BikeStatus.value == value).limit(1)) == 0:
            BikeStatus.create(the_key=the_key, value=value)

    check_or_create_bike_status(0, 'available')
    check_or_create_bike_status(1, 'in cart')
    check_or_create_bike_status(2, 'sold')

    # this is for demo code
    def check_or_create_bike_types(**kwargs):
        if len(BikeType.select().where(BikeType.title == kwargs["title"]).limit(1)) == 0:
            BikeType.create(
                title=kwargs.get("title"),
                description=kwargs.get("description"),
                stars=kwargs.get("stars"),
                created_on=datetime.datetime.now(tz=None),
            )

    check_or_create_bike_types(title="Abc", description="Description abc", stars=3)
    check_or_create_bike_types(title="Def", description="Description def", stars=3)
    check_or_create_bike_types(title="cDe", description="Description cde", stars=4)

    db.close()


seed_relational_db()
