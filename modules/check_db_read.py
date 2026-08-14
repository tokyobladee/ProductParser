from pprint import pprint

from load_django import *
from parser_app.models import Product


def serialize_product(product):
    return {
        field.name: getattr(product, field.name)
        for field in Product._meta.fields
    }


def main():
    product = (
        Product.objects.filter(product_code="DJANGO-INTEGRATION-CHECK")
        .order_by("id")
        .first()
    )
    if product is None:
        raise LookupError("Django integration check record does not exist")
    pprint(serialize_product(product))


if __name__ == "__main__":
    main()
