import re
import sys
from pprint import pprint

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from load_django import *
from browser_xpaths import (
    CHARACTERISTIC_LABELS,
    CHARACTERISTIC_LABEL_XPATH,
    CHARACTERISTIC_ROW_VALUE_XPATH,
    CHARACTERISTIC_ROW_XPATH,
    CHARACTERISTIC_VALUE_XPATH,
    CHARACTERISTICS_XPATH,
    FIRST_RESULT_XPATH,
    HOME_PAGE_URL,
    HOME_PAGE_XPATH,
    IMAGE_URL_ATTRIBUTE,
    IMAGE_XPATH,
    MAIN_PRICE_XPATH,
    PRODUCT_CARD_XPATH,
    PRODUCT_CODE_XPATH,
    PRODUCT_NAME_XPATH,
    PROMOTIONAL_PRICE_XPATH,
    REGULAR_PRICE_XPATH,
    REVIEW_COUNT_XPATH,
    SEARCH_INPUT_XPATH,
    SEARCH_QUERY,
)
from parser_app.models import Product
from parser_app.product_data import build_product_data, validate_product_data


WAIT_TIMEOUT_SECONDS = 30


def clean_text(value):
    if value is None:
        return None

    cleaned_value = " ".join(value.replace("\u00a0", " ").split())
    cleaned_value = re.sub(r"\s+([,;])", r"\1", cleaned_value)
    return cleaned_value or None


def find_visible_element(container, xpath):
    for element in container.find_elements(By.XPATH, xpath):
        if element.is_displayed():
            return element
    return None


def extract_optional_text(container, xpath):
    try:
        for element in container.find_elements(By.XPATH, xpath):
            value = clean_text(element.get_attribute("textContent"))
            if value is not None:
                return value
        return None
    except StaleElementReferenceException:
        return None


def extract_price_data(driver):
    try:
        price_container = find_visible_element(driver, MAIN_PRICE_XPATH)
        if price_container is None:
            return None, None

        regular_price = extract_optional_text(price_container, REGULAR_PRICE_XPATH)
        promotional_price = extract_optional_text(
            price_container,
            PROMOTIONAL_PRICE_XPATH,
        )
        if regular_price is None:
            return promotional_price, None
        return regular_price, promotional_price
    except StaleElementReferenceException:
        return None, None


def extract_image_urls(driver):
    try:
        image_urls = list(
            dict.fromkeys(
                image.get_attribute(IMAGE_URL_ATTRIBUTE)
                for image in driver.find_elements(By.XPATH, IMAGE_XPATH)
                if image.get_attribute(IMAGE_URL_ATTRIBUTE)
            )
        )
        return image_urls or None
    except StaleElementReferenceException:
        return None


def extract_review_count(driver):
    review_text = extract_optional_text(driver, REVIEW_COUNT_XPATH)
    if review_text is None:
        return None

    match = re.search(r"\d+", review_text.replace("\u00a0", ""))
    return int(match.group()) if match else None


def xpath_literal(value):
    if '"' not in value:
        return f'"{value}"'
    if "'" not in value:
        return f"'{value}'"
    parts = value.split('"')
    return "concat(" + ", '\"', ".join(f'"{part}"' for part in parts) + ")"


def extract_characteristic(container, label):
    if container is None:
        return None

    value_xpath = CHARACTERISTIC_VALUE_XPATH.format(label=xpath_literal(label))
    try:
        value_element = container.find_element(By.XPATH, value_xpath)
        return clean_text(value_element.get_attribute("textContent"))
    except (NoSuchElementException, StaleElementReferenceException):
        return None


def extract_characteristics(container):
    if container is None:
        return None

    characteristics = {}
    try:
        rows = container.find_elements(By.XPATH, CHARACTERISTIC_ROW_XPATH)
        for row in rows:
            label_element = row.find_element(By.XPATH, CHARACTERISTIC_LABEL_XPATH)
            label = clean_text(label_element.get_attribute("textContent"))
            if label is None:
                continue
            value_element = row.find_element(By.XPATH, CHARACTERISTIC_ROW_VALUE_XPATH)
            characteristics[label] = clean_text(value_element.get_attribute("textContent"))
    except StaleElementReferenceException:
        return characteristics or None
    return characteristics or None


def find_characteristics_container(driver):
    containers = driver.find_elements(By.XPATH, CHARACTERISTICS_XPATH)
    if not containers:
        return None
    return max(
        containers,
        key=lambda container: len(
            container.find_elements(By.XPATH, CHARACTERISTIC_ROW_XPATH)
        ),
    )


def open_product_page(driver, wait):
    driver.get(HOME_PAGE_URL)
    wait.until(expected_conditions.presence_of_element_located((By.XPATH, HOME_PAGE_XPATH)))
    search_input = wait.until(
        expected_conditions.element_to_be_clickable((By.XPATH, SEARCH_INPUT_XPATH))
    )
    search_input.send_keys(SEARCH_QUERY, Keys.ENTER)
    first_result = wait.until(
        expected_conditions.presence_of_element_located((By.XPATH, FIRST_RESULT_XPATH))
    )
    product_url = first_result.get_attribute("href")
    if not product_url:
        raise RuntimeError("The first search result does not contain a URL")
    driver.get(product_url)
    wait.until(
        expected_conditions.presence_of_element_located((By.XPATH, PRODUCT_CARD_XPATH))
    )


def extract_product_data(driver):
    product_data = build_product_data(
        Product.ParserType.SELENIUM.value,
        driver.current_url,
    )
    characteristics_container = find_characteristics_container(driver)
    regular_price, promotional_price = extract_price_data(driver)

    product_data["full_name"] = extract_optional_text(driver, PRODUCT_NAME_XPATH)
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
    product_data["image_urls"] = extract_image_urls(driver)
    product_data["product_code"] = extract_optional_text(driver, PRODUCT_CODE_XPATH)
    product_data["review_count"] = extract_review_count(driver)
    product_data["screen_diagonal"] = extract_characteristic(
        characteristics_container,
        CHARACTERISTIC_LABELS["screen_diagonal"],
    )
    product_data["display_resolution"] = extract_characteristic(
        characteristics_container,
        CHARACTERISTIC_LABELS["display_resolution"],
    )
    product_data["characteristics"] = extract_characteristics(
        characteristics_container,
    )
    return validate_product_data(product_data)


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    driver = create_driver()
    wait = WebDriverWait(driver, WAIT_TIMEOUT_SECONDS)
    try:
        open_product_page(driver, wait)
        product_data = extract_product_data(driver)
        pprint(product_data, sort_dicts=False)
        product, created = Product.objects.get_or_create(**product_data)
        pprint({"created": created, "product_id": product.pk})
    except TimeoutException as error:
        raise RuntimeError("The browser scenario did not finish in time") from error
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
