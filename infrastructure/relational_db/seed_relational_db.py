import datetime

from constants import UserRoleName, BikeStatusKeys
from infrastructure.relational_db import db
from infrastructure.relational_db.models import Role, BikeStatus, BikeType, User, UserRole


def seed_relational_db(use_test_data: bool):
    db.connect()

    def check_or_create_role(name):
        if len(Role.select().where(Role.name == name).limit(1)) == 0:
            Role.create(name=name, created_on=datetime.datetime.now(tz=None))

    check_or_create_role(UserRoleName.admin)
    check_or_create_role(UserRoleName.user)
    check_or_create_role(UserRoleName.guest)

    def check_or_create_bike_status(the_key, value):
        if len(BikeStatus.select().where(BikeStatus.value == value).limit(1)) == 0:
            BikeStatus.create(the_key=the_key, value=value)

    check_or_create_bike_status(BikeStatusKeys.available, 'available')
    check_or_create_bike_status(BikeStatusKeys.in_cart, 'in cart')
    check_or_create_bike_status(BikeStatusKeys.sold, 'sold')

    # ====================================
    # DEMO DATA - START

    if use_test_data is True:
        def check_or_create_bike_type(**kwargs):
            if len(BikeType.select().where(BikeType.title == kwargs["title"]).limit(1)) == 0:
                BikeType.create(
                    title=kwargs.get("title"),
                    description=kwargs.get("description"),
                    stars=kwargs.get("stars"),
                    created_on=datetime.datetime.now(tz=None),
                )

        check_or_create_bike_type(title="Abc", description="Description abc", stars=3)
        check_or_create_bike_type(title="Def", description="Description def", stars=3)
        check_or_create_bike_type(title="cDe", description="Description cde", stars=4)

        def check_or_create_user(**kwargs):
            if len(User.select().where(User.email == kwargs["email"]).limit(1)) == 0:
                User.create(email=kwargs.get("email"), created_on=datetime.datetime.now(tz=None))

        check_or_create_user(email="zeka.rum@gmail.com")
        check_or_create_user(email="user@test.com")
        check_or_create_user(email="guest@test.com")

        def check_or_create_user_role_pair(**kwargs):
            user = User.select().where(User.email == kwargs["email"]).limit(1)[0]
            role = Role.select().where(Role.name == kwargs["role_name"]).limit(1)[0]
            if len(UserRole.select().where(UserRole.user_id == user.id and UserRole.role_id == role.id).limit(1)) == 0:
                UserRole.create(user_id=user.id, role_id=role.id, created_on=datetime.datetime.now(tz=None))

        check_or_create_user_role_pair(email="zeka.rum@gmail.com", role_name=UserRoleName.admin)
        check_or_create_user_role_pair(email="user@test.com", role_name=UserRoleName.user)
        check_or_create_user_role_pair(email="guest@test.com", role_name=UserRoleName.guest)

    # DEMO DATA - END
    # ====================================

    db.close()


seed_relational_db(True)
