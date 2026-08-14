PRODUCT_NAME_SELECTOR = "h1.main-title[data-pid]"
MAIN_PRICE_SELECTOR = (
    "div.br-pr-price.main-price-block[data-series-product-id='0']"
)
REGULAR_PRICE_SELECTOR = "div.br-pr-op div.price-wrapper"
CURRENT_PRICE_SELECTOR = "div.br-pr-np div.price-wrapper"
IMAGE_SELECTOR = (
    "#br-product-modal img.dots-image[data-big-picture-src]"
)
IMAGE_URL_ATTRIBUTE = "data-big-picture-src"
PRODUCT_CODE_SELECTOR = "#product_code .br-pr-code-val"
REVIEW_COUNT_SELECTOR = "a.reviews-count[href='#reviews-list'] span"
CHARACTERISTICS_SELECTOR = "#br-characteristics .br-pr-chr"
CHARACTERISTIC_GROUP_SELECTOR = ".br-pr-chr-item"
CHARACTERISTIC_ROW_SELECTOR = ".br-pr-chr-item > div > div"

CHARACTERISTIC_LABELS = {
    "color": "Колір",
    "memory_capacity": "Вбудована пам'ять",
    "manufacturer": "Виробник",
    "screen_diagonal": "Діагональ екрану",
    "display_resolution": "Роздільна здатність екрану",
}
