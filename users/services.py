import os

import stripe

STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")


stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product):
    """Создаем продукт"""

    product = stripe.Product.create(name=product.name)
    return product


def create_stripe_price(amount, product):
    """Создает цену в страйпе"""
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": product.get("name")},
    )
    return price


def create_stripe_session(price):
    """Создает сессию на оплату в stripe"""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/users/payments/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
