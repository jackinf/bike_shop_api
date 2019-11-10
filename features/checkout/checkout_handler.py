from functools import reduce

import stripe
from aiohttp import web

from features.auth.auth_dao import AuthDao
from features.carts.cart_dao import CartDao
from helpers import extract_email_from_request


class CheckoutHandler(CartDao, AuthDao):
    async def handle_get_summary(self, request):
        user, error = await self._get_current_user(request)
        if error is not None:
            return web.json_response({"error": error}, status=400)

        bikes = await super().dao_get_items_from_cart(user.id)
        total_sum = reduce(lambda a, b: a + b, map(lambda bike: bike["selling_price"], bikes)) if len(bikes) > 0 else 0

        items = list(map(lambda bike: {
            "title": bike["title"],
            "description": "some description",
            "price": bike["selling_price"],
        }, bikes))

        return web.json_response({
            "items": items,
            "total_sum": total_sum,
            "shipping": {
                "name": "John Smith",
                "address_line_1": "address_line_1_123",
                "address_line_2": "address_line_2_123",
                "city": "city123",
                "state_province_region": "state_province_region123",
                "postal_code": "postal_code123",
                "country": "country123",
            }
        })

    async def handle_finalize_order(self, request):
        session_id = request.rel_url.query["sessionId"]

    async def _get_current_user(self, request):
        email = extract_email_from_request(request)
        if email is None:
            return None, "`email` query parameter must be provided"
        user = await super().dao_get_user_by_email(email)
        if user is None:
            return None, f"User with email {email} was not found"
        return user, None