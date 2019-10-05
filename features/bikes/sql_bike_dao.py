import random
from datetime import datetime

from dal.relational_db import db
from dal.relational_db.models import Bike, BikeType
from features.bikes.bike_dao import BikeDao
from helpers import async_wrapper, from_date_to_str


class SqlBikeDao(BikeDao):
    def __enter__(self):
        db.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        db.close()

    @async_wrapper
    def dao_search_bikes(self, page, rows_per_page, order_direction, order_column, filter_keyword):
        query = Bike.select(Bike, BikeType).join(BikeType)

        sort_options = {
            "purchase_price": lambda ref: ref.order_by(Bike.purchase_price if order_direction == 'desc' else Bike.purchase_price.desc()),
            "selling_price": lambda ref: ref.order_by(Bike.selling_price if order_direction == 'desc' else Bike.selling_price.desc()),
            "status_key": lambda ref: ref.order_by(Bike.status_key if order_direction == 'desc' else Bike.status_key.desc()),
            "created_on": lambda ref: ref.order_by(Bike.created_on if order_direction == 'desc' else Bike.created_on.desc()),
        }

        if order_column in sort_options:
            query = sort_options[order_column](query)
        else:
            query = sort_options["created_on"](query)

        if filter_keyword is not None:
            query = query.where(Bike.bike_type_id.title.contains(filter_keyword))

        # Page numbers are 1-based, so appending 1 to page
        query = query.paginate(page + 1, rows_per_page).prefetch(BikeType)

        results = []
        for item in query:
            result = {
                "id": str(item.id),
                "title": item.bike_type_id.title,
                "created_on": from_date_to_str(item.created_on)
            }

            try:
                result["purchase_price"] = float(item.purchase_price)
            except:
                pass

            try:
                result["selling_price"] = float(item.selling_price)
            except:
                pass

            results.append(result)

        total = Bike.select().count()
        return results, total

    @async_wrapper
    def dao_add_bike(self, bike) -> str:
        return self._add_bike(bike)

    # TODO: change argument `bike_id` to `bike: Bike`
    @async_wrapper
    def dao_remove_bike(self, bike_id):
        Bike.get(bike_id).delete_instance()

    @async_wrapper
    def dao_delete_all_bikes(self):
        Bike.delete().execute()

    @async_wrapper
    def dao_generate_bikes(self, number):
        for i in range(0, number):
            self._add_bike({
                "bike_type_id": "4c9c987c-e798-11e9-a446-0242ac110002",
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