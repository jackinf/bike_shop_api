from peewee import Model, CharField, DateTimeField, IntegerField, DecimalField, UUIDField, SmallIntegerField, \
    ForeignKeyField, CompositeKey

from dal.relational_db import db


class BaseModel(Model):
    id = UUIDField(primary_key=True)
    created_on = DateTimeField()
    updated_on = DateTimeField()
    created_by = UUIDField()    # TOOD: fkey
    updated_by = UUIDField()    # TOOD: fkey

    class Meta:
        database = db


class User(BaseModel):
    email = CharField()
    name = CharField()

    class Meta:
        database = db
        table_name = 'user'


class Role(BaseModel):
    name = CharField()

    class Meta:
        database = db
        table_name = 'role'


class UserRole(Model):
    user_id = ForeignKeyField(User, backref="user_roles", column_name="user_id")
    role_id = ForeignKeyField(Role, backref="user_roles", column_name="role_id")

    class Meta:
        database = db
        primary_key = CompositeKey('user_id', 'role_id')
        table_name = 'user_role'


class BikeStatus(Model):
    the_key = SmallIntegerField(primary_key=True, column_name='id')
    value = CharField()

    class Meta:
        database = db
        table_name = 'bike_status'


class BikeType(BaseModel):
    title = CharField()
    description = CharField()
    stars = IntegerField()

    class Meta:
        database = db
        table_name = 'bike_type'


class Bike(BaseModel):
    bike_type = ForeignKeyField(BikeType, backref="bikes", column_name='bike_type_id')
    purchase_price = DecimalField()
    selling_price = DecimalField()
    # status_key = ForeignKeyField(BikeStatus, backref="bikes")  # TODO: fix
    user_id = ForeignKeyField(User, backref="bikes", column_name='user_id')

    class Meta:
        database = db
        table_name = 'bike'
