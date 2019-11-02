from infrastructure.relational_db.models import Bike


class BikeDao:
    async def dao_search_bike_types(self, search_parameters):
        pass

    async def dao_search_bikes(self, search_parameters):
        pass

    async def dao_get_bike(self, bike) -> Bike:  # TODO: change to DB-neutral model
        pass

    async def dao_add_bike(self, bike) -> str:
        pass

    async def dao_update_bike(self, bike):
        pass

    async def dao_remove_bike(self, bike_id):
        pass

    async def dao_generate_bikes(self, number):
        pass

    async def dao_delete_all_bikes(self):
        pass
