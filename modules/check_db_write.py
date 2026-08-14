from pprint import pprint

from load_django import *
from parser_app.models import Product


def build_product_data():
    return {
        "parser_type": None,
        "source_url": "https://example.com/django-integration-check",
        "full_name": "Django Integration Check",
        "color": None,
        "memory_capacity": None,
        "manufacturer": None,
        "regular_price": None,
        "promotional_price": None,
        "image_urls": ["https://example.com/django-integration-check.jpg"],
        "product_code": "DJANGO-INTEGRATION-CHECK",
        "review_count": None,
        "screen_diagonal": None,
        "display_resolution": None,
        "characteristics": {"purpose": "Django integration check"},
    }


def main():
    product_data = build_product_data()
    product, created = Product.objects.get_or_create(**product_data)
    pprint(
        {
            "created": created,
            "product_id": product.pk,
            "product_code": product.product_code,
        }
    )


if __name__ == "__main__":
    main()
