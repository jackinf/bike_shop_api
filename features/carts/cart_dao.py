from abc import abstractmethod


class CartDao:

    @abstractmethod
    def get_single_cart(self, cart_id):
        pass

    @abstractmethod
    def get_single_bike(self, bike_id):  # TODO: Move to BikeDao
        pass

    @abstractmethod
    def get_items_from_cart(self, cart_id):
        pass

    @abstractmethod
    def find_single_cart(self, email):
        pass

    @abstractmethod
    def find_single_item_in_cart(self, items_in_cart, bike_key):
        pass

    @abstractmethod
    def add_item_into_cart(self, cart_id, document):
        pass

    @abstractmethod
    def delete_single_item_from_cart(self, cart_id, bike_id):
        pass
