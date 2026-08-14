import os
import re
import sys
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from load_django import *
from parser_app.models import Product
from parser_app.product_data import build_product_data, validate_product_data
from requests_bs4_selectors import (
    CHARACTERISTIC_LABELS,
    CHARACTERISTIC_ROW_SELECTOR,
    CHARACTERISTICS_SELECTOR,
    CURRENT_PRICE_SELECTOR,
    IMAGE_SELECTOR,
    IMAGE_URL_ATTRIBUTE,
    MAIN_PRICE_SELECTOR,
    PRODUCT_CODE_SELECTOR,
    PRODUCT_NAME_SELECTOR,
    REGULAR_PRICE_SELECTOR,
    REVIEW_COUNT_SELECTOR,
)


PRODUCT_URL = os.getenv(
    "REQUESTS_PRODUCT_URL",
    (
        "https://brain.com.ua/ukr/"
        "Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_"
        "Black_Titanium-p1145443.html"
    ),
)

REQUEST_HEADERS = {
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Referer": "https://brain.com.ua/ukr/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/139.0.0.0 Safari/537.36"
    ),
}

REQUEST_COOKIES = {}
REQUEST_TIMEOUT_SECONDS = 30


def build_session():
    retry_policy = Retry(
        total=2,
        connect=2,
        read=2,
        status=2,
        backoff_factor=1,
        status_forcelist=(502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        raise_on_status=False,
    )
    session = requests.Session()
    session.headers.update(REQUEST_HEADERS)
    session.cookies.update(REQUEST_COOKIES)
    session.mount("https://", HTTPAdapter(max_retries=retry_policy))
    return session


def fetch_product_page(session, url):
    response = session.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_text(container, selector):
    if container is None:
        return None

    element = container.select_one(selector)
    return clean_element_text(element)


def clean_element_text(element):
    if element is None:
        return None

    value = " ".join(
        element.get_text(" ", strip=True).replace("\u00a0", " ").split()
    )
    value = re.sub(r"\s+([,;])", r"\1", value)
    return value or None


def extract_characteristic(characteristics_container, label):
    if characteristics_container is None:
        return None

    label_element = characteristics_container.find(
        "span",
        string=lambda text: text and text.strip() == label,
    )
    if label_element is None:
        return None

    value_element = label_element.find_next_sibling("span")
    if value_element is None:
        return None

    return clean_element_text(value_element)


def extract_prices(soup):
    price_container = soup.select_one(MAIN_PRICE_SELECTOR)
    regular_price = extract_text(price_container, REGULAR_PRICE_SELECTOR)
    current_price = extract_text(price_container, CURRENT_PRICE_SELECTOR)

    if regular_price is None:
        return current_price, None

    return regular_price, current_price


def extract_image_urls(soup):
    image_urls = list(
        dict.fromkeys(
            image.get(IMAGE_URL_ATTRIBUTE)
            for image in soup.select(IMAGE_SELECTOR)
            if image.get(IMAGE_URL_ATTRIBUTE)
        )
    )
    return image_urls or None


def extract_review_count(soup):
    review_text = extract_text(soup, REVIEW_COUNT_SELECTOR)
    if review_text is None:
        return None

    review_match = re.search(r"\d+", review_text.replace("\u00a0", ""))
    return int(review_match.group()) if review_match else None


def extract_characteristics(characteristics_container):
    if characteristics_container is None:
        return None

    characteristics = {}
    for row in characteristics_container.select(CHARACTERISTIC_ROW_SELECTOR):
        label_element = row.find("span", recursive=False)
        if label_element is None:
            continue

        label = clean_element_text(label_element)
        if not label:
            continue

        value_element = label_element.find_next_sibling("span")
        characteristics[label] = clean_element_text(value_element)

    return characteristics or None


def extract_product_data(soup, source_url):
    product_data = build_product_data(
        Product.ParserType.REQUESTS_BS4.value,
        source_url,
    )
    characteristics_container = soup.select_one(CHARACTERISTICS_SELECTOR)
    regular_price, promotional_price = extract_prices(soup)

    product_data["full_name"] = extract_text(soup, PRODUCT_NAME_SELECTOR)
    product_data["color"] = extract_characteristic(
        characteristics_container,
        CHARACTERISTIC_LABELS["color"],
    )
    product_data["memory_capacity"] = extract_characteristic(
        characteristics_container,
        CHARACTERISTIC_LABELS["memory_capacity"],
    )
    product_data["manufacturer"] = extract_characteristic(
        characteristics_container,
        CHARACTERISTIC_LABELS["manufacturer"],
    )
    product_data["regular_price"] = regular_price
    product_data["promotional_price"] = promotional_price
    product_data["image_urls"] = extract_image_urls(soup)
    product_data["product_code"] = extract_text(soup, PRODUCT_CODE_SELECTOR)
    product_data["review_count"] = extract_review_count(soup)
    product_data["screen_diagonal"] = extract_characteristic(
        characteristics_container,
        CHARACTERISTIC_LABELS["screen_diagonal"],
    )
    product_data["display_resolution"] = extract_characteristic(
        characteristics_container,
        CHARACTERISTIC_LABELS["display_resolution"],
    )
    product_data["characteristics"] = extract_characteristics(
        characteristics_container
    )
    return validate_product_data(product_data)


def main():
    sys.stdout.reconfigure(encoding="utf-8")

    with build_session() as session:
        soup = fetch_product_page(session, PRODUCT_URL)

    product_data = extract_product_data(soup, PRODUCT_URL)
    pprint(product_data, sort_dicts=False)
    product, created = Product.objects.get_or_create(**product_data)
    pprint({"created": created, "product_id": product.pk})


if __name__ == "__main__":
    main()
