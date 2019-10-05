from peewee import Model, CharField, DateTimeField, IntegerField, DecimalField, UUIDField, SmallIntegerField, \
    ForeignKeyField

from dal.relational_db import db


class BaseModel(Model):
    id = UUIDField(primary_key=True)
    created_on = DateTimeField()
    updated_on = DateTimeField()
    created_by = UUIDField()
    updated_by = UUIDField()

    class Meta:
        database = db


class BikeType(BaseModel):
    title = CharField()
    description = CharField()
    stars = IntegerField()

    class Meta:
        database = db
        table_name = 'bike_type'


class Bike(BaseModel):
    bike_type_id = ForeignKeyField(BikeType, backref='bikes')
    purchase_price = DecimalField()
    selling_price = DecimalField()
    status_key = SmallIntegerField()
    user_id = UUIDField()

    class Meta:
        database = db
        table_name = 'bike'


class BikeStatus(Model):
    the_key = SmallIntegerField(primary_key=True, column_name='id')
    value = CharField()

    class Meta:
        database = db
        table_name = 'bike_status'


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
    user_id = UUIDField()
    role_id = UUIDField()

    class Meta:
        database = db
        table_name = 'user_role'

