from helpers import async_wrapper


class CartDao:
    async def get_single_cart(self, cart_id):
        pass

    async def get_single_bike(self, bike_id):  # TODO: Move to BikeDao
        pass

    async def get_items_from_cart(self, cart_id):
        pass

    async def find_single_cart(self, email):
        pass

    async def find_single_item_in_cart(self, items_in_cart, bike_key):
        pass

    async def add_item_into_cart(self, cart_id, document):
        pass

    async def delete_single_item_from_cart(self, cart_id, bike_id):
        pass
