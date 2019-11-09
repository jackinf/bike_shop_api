from functools import reduce

import stripe
from typing import Tuple, Optional
from aiohttp import web

from features.auth.auth_dao import AuthDao
from features.carts.cart_dao import CartDao
from helpers import extract_email_from_request


class PaymentHandler(CartDao, AuthDao):
    async def handle_create_payment_indent(self, request):
        (total, error) = await self._get_total_for_current_user(request)
        if error is not None:
            return web.json_response({"error": error}, status=400)
        if total <= 0:
            return web.json_response({"error": "Total amount is 0 or less"}, status=400)

        intent = stripe.PaymentIntent.create(amount=int(total), currency='eur')
        secret = str(intent.client_secret)
        return web.json_response({"clientSecret": f"{secret}"})

    async def _get_total_for_current_user(self, request) -> Tuple[Optional[float], Optional[str]]:
        email = extract_email_from_request(request)
        if email is None:
            return None, "`email` query parameter must be provided"
        user = await super().dao_get_user_by_email(email)
        if user is None:
            return None, f"User with email {email} was not found"
        bikes = await super().dao_get_items_from_cart(user.id)
        total_sum = reduce(lambda a, b: a + b, map(lambda bike: bike["selling_price"], bikes)) if len(bikes) > 0 else 0
        return total_sum, None

