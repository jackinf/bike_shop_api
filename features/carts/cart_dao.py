class CartDao:
    async def dao_get_single_cart_item(self, cart_id):
        pass

    async def dao_get_items_from_cart(self, cart_id):
        pass

    async def dao_find_single_cart(self, email):
        pass

    async def dao_find_single_item_in_cart(self, items_in_cart, bike_key):
        pass

    async def dao_add_item_into_cart(self, cart_id, document):
        pass

    async def dao_delete_single_item_from_cart(self, cart_id, bike_id):
        pass
