from django.test import SimpleTestCase

from parser_app.models import Product
from parser_app.product_data import (
    OPTIONAL_TEXT_KEYS,
    PRODUCT_DATA_KEYS,
    build_product_data,
    validate_product_data,
)


class ProductDataContractTests(SimpleTestCase):
    def build_valid_product_data(self):
        product_data = build_product_data(
            Product.ParserType.REQUESTS_BS4,
            "https://brain.com.ua/product",
        )
        product_data.update(
            {
                "full_name": "Apple iPhone 15 128GB Black",
                "color": "Black",
                "memory_capacity": "128 GB",
                "manufacturer": "Apple",
                "regular_price": "34 999 UAH",
                "promotional_price": "31 999 UAH",
                "image_urls": ["https://brain.com.ua/image.jpg"],
                "product_code": "123456",
                "review_count": 25,
                "screen_diagonal": "6.1 inches",
                "display_resolution": "2556x1179",
                "characteristics": {"Operating system": "iOS"},
            }
        )
        return product_data

    def test_contract_matches_product_model_fields(self):
        model_fields = {
            field.name for field in Product._meta.fields if field.name != "id"
        }

        self.assertEqual(model_fields, set(PRODUCT_DATA_KEYS))

    def test_builder_uses_same_keys_and_none_for_missing_values(self):
        for parser_type in Product.ParserType.values:
            with self.subTest(parser_type=parser_type):
                product_data = build_product_data(
                    parser_type,
                    "https://brain.com.ua/product",
                )

                self.assertEqual(tuple(product_data), PRODUCT_DATA_KEYS)
                for key in PRODUCT_DATA_KEYS[2:]:
                    self.assertIsNone(product_data[key])

    def test_valid_product_data_passes_unchanged(self):
        product_data = self.build_valid_product_data()

        self.assertIs(validate_product_data(product_data), product_data)

    def test_dictionary_must_have_exact_contract_keys(self):
        product_data = self.build_valid_product_data()
        product_data.pop("color")

        with self.assertRaises(ValueError):
            validate_product_data(product_data)

        product_data = self.build_valid_product_data()
        product_data["unexpected"] = None

        with self.assertRaises(ValueError):
            validate_product_data(product_data)

    def test_parser_type_and_source_url_are_required(self):
        with self.assertRaises(ValueError):
            build_product_data("unknown", "https://brain.com.ua/product")

        with self.assertRaises(TypeError):
            build_product_data(Product.ParserType.SELENIUM, "")

    def test_optional_text_values_are_strings_or_none(self):
        for key in OPTIONAL_TEXT_KEYS:
            with self.subTest(key=key):
                product_data = self.build_valid_product_data()
                product_data[key] = ""

                with self.assertRaises(TypeError):
                    validate_product_data(product_data)

                product_data[key] = None
                self.assertIs(validate_product_data(product_data), product_data)

    def test_review_count_is_a_non_negative_integer_or_none(self):
        for invalid_value in (-1, "25", True):
            with self.subTest(value=invalid_value):
                product_data = self.build_valid_product_data()
                product_data["review_count"] = invalid_value

                with self.assertRaises(TypeError):
                    validate_product_data(product_data)

        product_data = self.build_valid_product_data()
        product_data["review_count"] = None
        self.assertIs(validate_product_data(product_data), product_data)

    def test_image_urls_are_a_list_of_non_empty_strings_or_none(self):
        for invalid_value in ([], "https://brain.com.ua/image.jpg", [""]):
            with self.subTest(value=invalid_value):
                product_data = self.build_valid_product_data()
                product_data["image_urls"] = invalid_value

                with self.assertRaises(TypeError):
                    validate_product_data(product_data)

        product_data = self.build_valid_product_data()
        product_data["image_urls"] = None
        self.assertIs(validate_product_data(product_data), product_data)

    def test_characteristics_are_a_dictionary_or_none(self):
        invalid_values = ({}, [], {"": "value"}, {"Name": ""})
        for invalid_value in invalid_values:
            with self.subTest(value=invalid_value):
                product_data = self.build_valid_product_data()
                product_data["characteristics"] = invalid_value

                with self.assertRaises(TypeError):
                    validate_product_data(product_data)

        product_data = self.build_valid_product_data()
        product_data["characteristics"] = {"Optional value": None}
        self.assertIs(validate_product_data(product_data), product_data)
