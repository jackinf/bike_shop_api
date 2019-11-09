import stripe
from functools import reduce
from typing import Tuple, Optional, List
from aiohttp import web

from features.auth.auth_dao import AuthDao
from features.carts.cart_dao import CartDao
from helpers import extract_email_from_request


class PaymentHandler(CartDao, AuthDao):
    async def handle_create_payment_indent(self, request):
        (bikes, error) = await self._get_total_for_current_user(request)
        if error is not None:
            return web.json_response({"error": error}, status=400)
        total = reduce(lambda a, b: a + b, map(lambda bike: bike["selling_price"], bikes)) if len(bikes) > 0 else 0
        if total <= 0:
            return web.json_response({"error": "Total amount is 0 or less"}, status=400)

        # amount is being divided by 100 in Stripe's backend
        intent = stripe.PaymentIntent.create(amount=int(total * 100), currency='eur')
        secret = str(intent.client_secret)
        return web.json_response({"clientSecret": f"{secret}"})

    async def handle_create_standalone_checkout_session(self, request):
        success_url = request.rel_url.query['success_url']
        cancel_url = request.rel_url.query['cancel_url']
        (bikes, error) = await self._get_total_for_current_user(request)
        if error is not None:
            return web.json_response({"error": error}, status=400)

        line_items = list(map(lambda bike: {
            'name': bike['title'],
            'description': 'Some description',
            'images': [bike['image']],
            'amount': int(bike['selling_price'] * 100),  # amount is being divided by 100 in Stripe's backend
            'currency': 'eur',
            'quantity': 1,
        }, bikes))

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            success_url=success_url,
            cancel_url=cancel_url,
        )

        return web.json_response({"sessionId": session.id})

    async def _get_total_for_current_user(self, request) -> Tuple[Optional[List[any]], Optional[str]]:
        email = extract_email_from_request(request)
        if email is None:
            return None, "`email` query parameter must be provided"
        user = await super().dao_get_user_by_email(email)
        if user is None:
            return None, f"User with email {email} was not found"
        return await self._get_bikes_from_cart(user.id)

    async def _get_bikes_from_cart(self, user_id):
        bikes = await super().dao_get_items_from_cart(user_id)
        return bikes, None

