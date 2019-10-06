class CollectionName:
    bikes = "bikes"
    carts = "carts"


class UserRoleName:
    admin = "admin"
    user = "user"
    guest = "guest"


class HeaderKeys:
    authorization = "AUTHORIZATION"


class RequestContextKeys:
    auth_user = "auth_user"
    email = "email"


class BikeStatusKeys:
    available = 0
    in_cart = 1
    sold = 2
