import datetime
import random
from peewee import JOIN

from constants import UserRoleName, BikeStatusKeys
from infrastructure.relational_db import db
from infrastructure.relational_db.models import Role, BikeStatus, BikeType, User, UserRole, Bike, Cart


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

        bike_title_1 = "Abc"
        bike_title_2 = "Def"
        bike_title_3 = "cDe"
        check_or_create_bike_type(title=bike_title_1, description="Description abc", stars=3)
        check_or_create_bike_type(title=bike_title_2, description="Description def", stars=3)
        check_or_create_bike_type(title=bike_title_3, description="Description cde", stars=4)

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

        def check_or_create_bikes(**kwargs):
            bike_type = BikeType.select().where(BikeType.title == kwargs["title"]).limit(1)[0]
            if len(Bike.select().where(Bike.bike_type == bike_type.id).limit(1)) == 0:
                bike_status_titles = ['available', 'in cart', 'sold']
                bike_statuses = list(BikeStatus.select().where(BikeStatus.value in bike_status_titles))
                for i in range(0, random.choice([3, 4, 5])):
                    Bike.create(
                        bike_type=bike_type.id,
                        purchase_price=random.randint(200, 2000),
                        selling_price=random.randint(200, 2000),
                        status_key=random.choice(bike_statuses).the_key,
                        is_public=random.choice([True, False]),
                        created_on=datetime.datetime.now(tz=None)
                    )

        check_or_create_bikes(title=bike_title_1)
        check_or_create_bikes(title=bike_title_2)
        check_or_create_bikes(title=bike_title_3)

        def check_or_create_cart_item_for_first_available_bike(**kwargs):
            email = kwargs["email"]
            cart_already_exists_query = Cart.select().join(User).where(Cart.user_id.email == email).limit(1)
            if len(cart_already_exists_query) == 0:
                get_first_bike_not_in_cart_query = Bike \
                    .select() \
                    .join_from(Bike, Cart, JOIN.LEFT_OUTER) \
                    .where(Cart.id == None)
                if len(get_first_bike_not_in_cart_query) > 0:
                    bike = get_first_bike_not_in_cart_query[0]
                    user = User.select().where(User.email == email).limit(1)[0]
                    Cart.create(user_id=user.id, bike_id=bike.id, created_on=datetime.datetime.now(tz=None))

        check_or_create_cart_item_for_first_available_bike(email="zeka.rum@gmail.com")

    # DEMO DATA - END
    # ====================================

    db.close()


seed_relational_db(True)
