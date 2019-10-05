class BikeDao:
    async def dao_search_bikes(self, page, rows_per_page, order_direction, order_column, filter_keyword):
        pass

    async def get_all_bikes(self):
        pass

    async def dao_add_bike(self, bike) -> str:
        pass

    async def dao_remove_bike(self, bike_id):
        pass

    async def dao_generate_bikes(self, number):
        pass

    async def dao_delete_all_bikes(self):
        pass
