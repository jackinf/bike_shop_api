import random
from datetime import datetime
from peewee import JOIN
from dal.relational_db import db
from dal.relational_db.models import Bike, BikeType, User, BikeStatus
from features.bikes.bike_dao import BikeDao
from decorators.async_wrapper import async_wrapper
from helpers import from_date_to_str


class SqlBikeDao(BikeDao):
    def __enter__(self):
        db.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        db.close()

    @async_wrapper
    def dao_search_bike_types(self, search_parameters):
        page = search_parameters.get('page')
        rows_per_page = search_parameters.get('rows_per_page')
        order_direction = search_parameters.get('order_direction')
        order_column = search_parameters.get('order_column')
        filter_keyword = search_parameters.get('filter_keyword')

        sort_options = {
            "title": lambda ref: ref.order_by(
                BikeType.title.desc() if order_direction == 'desc' else BikeType.title
            ),
            "description": lambda ref: ref.order_by(
                BikeType.description.desc() if order_direction == 'desc' else BikeType.description
            ),
            "stars": lambda ref: ref.order_by(
                BikeType.stars.desc() if order_direction == 'desc' else BikeType.stars
            ),
            "created_on": lambda ref: ref.order_by(
                BikeType.created_on.desc() if order_direction == 'desc' else BikeType.created_on
            ),
        }

        query = self._apply_sort(BikeType.select(), order_column, sort_options)
        if filter_keyword is not None and filter_keyword != '':
            query = query.where(BikeType.title.contains(filter_keyword))
        query = query.paginate(page + 1, rows_per_page)
        results = self._map_dao_search_bike_types_query_results(query)
        total = BikeType.select().count()
        return results, total

    @async_wrapper
    def dao_search_bikes(self, search_parameters):
        page = search_parameters.get('page')
        rows_per_page = search_parameters.get('rows_per_page')
        order_direction = search_parameters.get('order_direction')
        order_column = search_parameters.get('order_column')
        filter_keyword = search_parameters.get('filter_keyword')
        bike_type_id = search_parameters.get('bike_type_id', None)
        is_public = search_parameters.get('is_public', None)

        query = Bike.select(Bike, BikeType)\
            .join(BikeType, JOIN.LEFT_OUTER, on=(Bike.bike_type == BikeType.id))\
            .join(User, JOIN.LEFT_OUTER, on=(Bike.user_id == User.id))\
            .join(BikeStatus, JOIN.LEFT_OUTER, on=(Bike.status_key == BikeStatus.the_key))

        sort_options = {
            "user": lambda ref: ref.order_by(
                Bike.user_id.email.desc() if order_direction == 'desc' else Bike.user_id.email
            ),
            "status": lambda ref: ref.order_by(
                Bike.status_key.value.desc() if order_direction == 'desc' else Bike.status_key.value
            ),
            "created_on": lambda ref: ref.order_by(
                Bike.created_on.desc() if order_direction == 'desc' else Bike.created_on
            ),
            "purchase_price": lambda ref: ref.order_by(
                Bike.purchase_price.desc() if order_direction == 'desc' else Bike.purchase_price
            ),
            "selling_price": lambda ref: ref.order_by(
                Bike.selling_price.desc() if order_direction == 'desc' else Bike.selling_price
            ),
        }

        query = self._apply_sort(query, order_column, sort_options)

        if filter_keyword is not None and filter_keyword != '':
            query = query.where(
                Bike.user_id.email.contains(filter_keyword) | Bike.status_key.value.contains(filter_keyword)
            )
        if bike_type_id is not None:
            query = query.where(Bike.bike_type == bike_type_id)
        if is_public is not None:
            query = query.where(Bike.is_public)

        # Page numbers are 1-based, so appending 1 to page
        query = query.paginate(page + 1, rows_per_page).prefetch(BikeType)
        results = self._map_dao_search_bikes_query_result(query)
        total = Bike.select().count()
        return results, total

    @async_wrapper
    def dao_get_bike(self, bike_id) -> Bike:
        return Bike.select().where(Bike.id == bike_id).limit(1)

    @async_wrapper
    def dao_add_bike(self, bike) -> str:
        return self._add_bike(bike)

    @async_wrapper
    def dao_update_bike(self, bike):
        bike.save()

    # TODO: change argument `bike_id` to `bike: Bike`
    @async_wrapper
    def dao_remove_bike(self, bike_id):
        Bike.get(bike_id).delete_instance()

    @async_wrapper
    def dao_delete_all_bikes(self):
        Bike.delete().execute()

    @async_wrapper
    def dao_generate_bikes(self, number):
        bike_type = BikeType.select().limit(1)[0]
        for i in range(0, number):
            self._add_bike({
                "bike_type_id": bike_type.id,
                "purchase_price": random.randint(100, 2000),
                "selling_price": random.randint(100, 2000),
                "status_key": random.choice([0, 1, 2]),
            })

    def _add_bike(self, bike):
        bike = Bike(
            bike_type_id=bike.get('bike_type_id', None),
            purchase_price=bike.get('purchase_price', None),
            selling_price=bike.get('selling_price', None),
            status_key=bike.get('status_key', None),
            user_id=bike.get('user_id', None),
            created_on=bike.get('created_on', datetime.now(tz=None))
        )
        bike.save()
        return bike.id

    def _map_dao_search_bike_types_query_results(self, query):
        results = []
        for item in query:
            result = {
                "id": str(item.id),
                "title": item.title,
                "stars": int(item.stars),
                "created_on": from_date_to_str(item.created_on)
            }
            results.append(result)
        return results

    def _map_dao_search_bikes_query_result(self, query):
        results = []
        for item in query:
            result = {
                "id": str(item.id),
                "is_public": item.is_public,
                "created_on": from_date_to_str(item.created_on)
            }

            try:
                result["user"] = item.user_id.email
            except:
                result["user"] = None

            try:
                result["status"] = item.status_key.value
            except:
                result["status"] = None

            try:
                result["purchase_price"] = float(item.purchase_price)
            except:
                pass

            try:
                result["selling_price"] = float(item.selling_price)
            except:
                pass

            results.append(result)
        return results

    def _apply_sort(self, query, order_column, sort_options):
        return sort_options[order_column](query) if order_column in sort_options else sort_options["created_on"](query)
