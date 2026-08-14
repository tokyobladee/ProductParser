import asyncio
import re
import sys
from pprint import pprint

from asgiref.sync import sync_to_async
from playwright.async_api import TimeoutError, async_playwright

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


WAIT_TIMEOUT_MILLISECONDS = 30000


def clean_text(value):
    if value is None:
        return None

    cleaned_value = " ".join(value.replace("\u00a0", " ").split())
    cleaned_value = re.sub(r"\s+([,;])", r"\1", cleaned_value)
    return cleaned_value or None


def xpath_literal(value):
    if '"' not in value:
        return f'"{value}"'
    if "'" not in value:
        return f"'{value}'"
    parts = value.split('"')
    return "concat(" + ", '\"', ".join(f'"{part}"' for part in parts) + ")"


async def extract_optional_text(container, xpath):
    locator = container.locator(f"xpath={xpath}")
    for index in range(await locator.count()):
        value = clean_text(await locator.nth(index).text_content())
        if value is not None:
            return value
    return None


async def extract_price_data(page):
    price_container = page.locator(f"xpath={MAIN_PRICE_XPATH}")
    if await price_container.count() == 0:
        return None, None

    regular_price = await extract_optional_text(
        price_container,
        REGULAR_PRICE_XPATH,
    )
    promotional_price = await extract_optional_text(
        price_container,
        PROMOTIONAL_PRICE_XPATH,
    )
    if regular_price is None:
        return promotional_price, None
    return regular_price, promotional_price


async def extract_image_urls(page):
    image_locator = page.locator(f"xpath={IMAGE_XPATH}")
    image_urls = []
    for index in range(await image_locator.count()):
        image_url = await image_locator.nth(index).get_attribute(
            IMAGE_URL_ATTRIBUTE
        )
        if image_url and image_url not in image_urls:
            image_urls.append(image_url)
    return image_urls or None


async def extract_review_count(page):
    review_text = await extract_optional_text(page, REVIEW_COUNT_XPATH)
    if review_text is None:
        return None

    match = re.search(r"\d+", review_text.replace("\u00a0", ""))
    return int(match.group()) if match else None


async def find_characteristics_container(page):
    containers = page.locator(f"xpath={CHARACTERISTICS_XPATH}")
    container_count = await containers.count()
    if container_count == 0:
        return None

    selected_container = containers.nth(0)
    selected_row_count = -1
    for index in range(container_count):
        container = containers.nth(index)
        row_count = await container.locator(
            f"xpath={CHARACTERISTIC_ROW_XPATH}"
        ).count()
        if row_count > selected_row_count:
            selected_container = container
            selected_row_count = row_count
    return selected_container


async def extract_characteristic(container, label):
    if container is None:
        return None

    value_xpath = CHARACTERISTIC_VALUE_XPATH.format(label=xpath_literal(label))
    return await extract_optional_text(container, value_xpath)


async def extract_characteristics(container):
    if container is None:
        return None

    characteristics = {}
    rows = container.locator(f"xpath={CHARACTERISTIC_ROW_XPATH}")
    for index in range(await rows.count()):
        row = rows.nth(index)
        label = await extract_optional_text(row, CHARACTERISTIC_LABEL_XPATH)
        if label is None:
            continue
        characteristics[label] = await extract_optional_text(
            row,
            CHARACTERISTIC_ROW_VALUE_XPATH,
        )
    return characteristics or None


async def open_product_page(page):
    await page.goto(HOME_PAGE_URL, wait_until="domcontentloaded")
    await page.locator(f"xpath={HOME_PAGE_XPATH}").wait_for()
    search_input = page.locator(f"xpath={SEARCH_INPUT_XPATH}")
    await search_input.click()
    await search_input.press_sequentially(SEARCH_QUERY, delay=50)
    first_result = page.locator(f"xpath={FIRST_RESULT_XPATH}").first
    await first_result.wait_for()
    product_url = await first_result.get_attribute("href")
    if not product_url:
        raise RuntimeError("The first search result does not contain a URL")
    await page.goto(product_url, wait_until="domcontentloaded")
    await page.locator(f"xpath={PRODUCT_CARD_XPATH}").first.wait_for(
        state="attached"
    )


async def extract_product_data(page):
    product_data = build_product_data(
        Product.ParserType.PLAYWRIGHT.value,
        page.url,
    )
    characteristics_container = await find_characteristics_container(page)
    regular_price, promotional_price = await extract_price_data(page)

    product_data["full_name"] = await extract_optional_text(
        page, PRODUCT_NAME_XPATH
    )
    product_data["color"] = await extract_characteristic(
        characteristics_container,
        CHARACTERISTIC_LABELS["color"],
    )
    product_data["memory_capacity"] = await extract_characteristic(
        characteristics_container,
        CHARACTERISTIC_LABELS["memory_capacity"],
    )
    product_data["manufacturer"] = await extract_characteristic(
        characteristics_container,
        CHARACTERISTIC_LABELS["manufacturer"],
    )
    product_data["regular_price"] = regular_price
    product_data["promotional_price"] = promotional_price
    product_data["image_urls"] = await extract_image_urls(page)
    product_data["product_code"] = await extract_optional_text(
        page, PRODUCT_CODE_XPATH
    )
    product_data["review_count"] = await extract_review_count(page)
    product_data["screen_diagonal"] = await extract_characteristic(
        characteristics_container,
        CHARACTERISTIC_LABELS["screen_diagonal"],
    )
    product_data["display_resolution"] = await extract_characteristic(
        characteristics_container,
        CHARACTERISTIC_LABELS["display_resolution"],
    )
    product_data["characteristics"] = await extract_characteristics(
        characteristics_container
    )
    return validate_product_data(product_data)


@sync_to_async
def save_product_data(product_data):
    return Product.objects.get_or_create(**product_data)


async def main():
    sys.stdout.reconfigure(encoding="utf-8")
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            channel="chrome", headless=False
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        page.set_default_timeout(WAIT_TIMEOUT_MILLISECONDS)
        try:
            await open_product_page(page)
            product_data = await extract_product_data(page)
            pprint(product_data, sort_dicts=False)
            product, created = await save_product_data(product_data)
            pprint({"created": created, "product_id": product.pk})
        except TimeoutError as error:
            raise RuntimeError(
                "The browser scenario did not finish in time"
            ) from error
        finally:
            await page.close()
            await context.close()
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
