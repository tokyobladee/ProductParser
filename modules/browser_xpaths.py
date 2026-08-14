import os


HOME_PAGE_URL = "https://brain.com.ua/ukr/"
SEARCH_QUERY = os.getenv("BROWSER_SEARCH_QUERY", "Apple iPhone 15 128GB Black")

HOME_PAGE_XPATH = "//a[contains(@class, 'svg-logo-gray') and @href='https://brain.com.ua/ukr/']"
SEARCH_INPUT_XPATH = "//div[contains(@class, 'header-bottom-in')]//input[contains(@class, 'quick-search-input')]"
SEARCH_BUTTON_XPATH = "//input[contains(@class, 'qsr-submit')]"
FIRST_RESULT_XPATH = (
    "//div[contains(@class, 'quick-search-res')]//a[contains(@class, 'qsr-link')] | "
    "//a[contains(normalize-space(), 'Apple iPhone 15 128GB Black (MTP03)')]"
)
PRODUCT_CARD_XPATH = "//h1[contains(@class, 'main-title') and @data-pid]"
PRODUCT_NAME_XPATH = PRODUCT_CARD_XPATH
MAIN_PRICE_XPATH = "//div[contains(@class, 'main-price-block') and @data-series-product-id='0']"
REGULAR_PRICE_XPATH = ".//div[contains(@class, 'br-pr-op')]//div[contains(@class, 'price-wrapper')]"
PROMOTIONAL_PRICE_XPATH = ".//div[contains(@class, 'br-pr-np')]//div[contains(@class, 'price-wrapper')]"
IMAGE_XPATH = "//div[@id='br-product-modal']//img[@data-big-picture-src]"
IMAGE_URL_ATTRIBUTE = "data-big-picture-src"
PRODUCT_CODE_XPATH = "//div[@id='product_code']//span[contains(@class, 'br-pr-code-val')]"
REVIEW_COUNT_XPATH = "//a[contains(@class, 'scroll-to-element') and contains(@class, 'reviews-count')]//span"
CHARACTERISTICS_XPATH = "//div[@id='br-characteristics']"
CHARACTERISTIC_ROW_XPATH = ".//div[contains(@class, 'br-pr-chr-item')]/div/div"
CHARACTERISTIC_LABEL_XPATH = "./span[not(preceding-sibling::span)]"
CHARACTERISTIC_ROW_VALUE_XPATH = "./span[preceding-sibling::span]"
CHARACTERISTIC_VALUE_XPATH = ".//span[normalize-space()={label}]/following-sibling::span"

CHARACTERISTIC_LABELS = {
    "color": "Колір",
    "memory_capacity": "Вбудована пам'ять",
    "manufacturer": "Виробник",
    "screen_diagonal": "Діагональ екрану",
    "display_resolution": "Роздільна здатність екрану",
}
