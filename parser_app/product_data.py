from typing import TypedDict

from parser_app.models import Product


class ProductData(TypedDict):
    parser_type: str
    source_url: str
    full_name: str | None
    color: str | None
    memory_capacity: str | None
    manufacturer: str | None
    regular_price: str | None
    promotional_price: str | None
    image_urls: list[str] | None
    product_code: str | None
    review_count: int | None
    screen_diagonal: str | None
    display_resolution: str | None
    characteristics: dict[str, str | None] | None


PRODUCT_DATA_KEYS = (
    "parser_type",
    "source_url",
    "full_name",
    "color",
    "memory_capacity",
    "manufacturer",
    "regular_price",
    "promotional_price",
    "image_urls",
    "product_code",
    "review_count",
    "screen_diagonal",
    "display_resolution",
    "characteristics",
)

OPTIONAL_TEXT_KEYS = (
    "full_name",
    "color",
    "memory_capacity",
    "manufacturer",
    "regular_price",
    "promotional_price",
    "product_code",
    "screen_diagonal",
    "display_resolution",
)

PARSER_TYPES = frozenset(Product.ParserType.values)


def build_product_data(parser_type: str, source_url: str) -> ProductData:
    product_data: ProductData = {
        "parser_type": parser_type,
        "source_url": source_url,
        "full_name": None,
        "color": None,
        "memory_capacity": None,
        "manufacturer": None,
        "regular_price": None,
        "promotional_price": None,
        "image_urls": None,
        "product_code": None,
        "review_count": None,
        "screen_diagonal": None,
        "display_resolution": None,
        "characteristics": None,
    }
    return validate_product_data(product_data)


def validate_product_data(product_data: object) -> ProductData:
    if not isinstance(product_data, dict):
        raise TypeError("Product data must be a dictionary")

    expected_keys = set(PRODUCT_DATA_KEYS)
    actual_keys = set(product_data)
    if actual_keys != expected_keys:
        missing_keys = sorted(expected_keys - actual_keys)
        extra_keys = sorted(actual_keys - expected_keys)
        raise ValueError(
            f"Product data keys do not match the contract: "
            f"missing={missing_keys}, extra={extra_keys}"
        )

    parser_type = product_data["parser_type"]
    if parser_type not in PARSER_TYPES:
        raise ValueError(f"Unsupported parser type: {parser_type}")

    source_url = product_data["source_url"]
    if not isinstance(source_url, str) or not source_url.strip():
        raise TypeError("source_url must be a non-empty string")

    for key in OPTIONAL_TEXT_KEYS:
        value = product_data[key]
        if value is not None and (
            not isinstance(value, str) or not value.strip()
        ):
            raise TypeError(f"{key} must be a non-empty string or None")

    review_count = product_data["review_count"]
    if review_count is not None and (
        isinstance(review_count, bool)
        or not isinstance(review_count, int)
        or review_count < 0
    ):
        raise TypeError("review_count must be a non-negative integer or None")

    image_urls = product_data["image_urls"]
    if image_urls is not None:
        if not isinstance(image_urls, list) or not image_urls:
            raise TypeError("image_urls must be a non-empty list or None")
        if any(
            not isinstance(image_url, str) or not image_url.strip()
            for image_url in image_urls
        ):
            raise TypeError("Every image URL must be a non-empty string")

    characteristics = product_data["characteristics"]
    if characteristics is not None:
        if not isinstance(characteristics, dict) or not characteristics:
            raise TypeError("characteristics must be a non-empty dictionary or None")
        for key, value in characteristics.items():
            if not isinstance(key, str) or not key.strip():
                raise TypeError("Every characteristic name must be a non-empty string")
            if value is not None and (
                not isinstance(value, str) or not value.strip()
            ):
                raise TypeError(
                    "Every characteristic value must be a non-empty string or None"
                )

    return product_data
