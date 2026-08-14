from django.contrib.postgres.fields import ArrayField
from django.db import models


class Product(models.Model):
    class ParserType(models.TextChoices):
        REQUESTS_BS4 = "requests_bs4", "Requests and BeautifulSoup"
        SELENIUM = "selenium", "Selenium"
        PLAYWRIGHT = "playwright", "Playwright"

    parser_type = models.CharField(
        max_length=32,
        choices=ParserType.choices,
        null=True,
        blank=True,
    )
    source_url = models.URLField(max_length=2048, null=True, blank=True)
    full_name = models.CharField(max_length=500, null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    memory_capacity = models.CharField(max_length=255, null=True, blank=True)
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    regular_price = models.CharField(max_length=100, null=True, blank=True)
    promotional_price = models.CharField(max_length=100, null=True, blank=True)
    image_urls = ArrayField(
        models.URLField(max_length=2048),
        null=True,
        blank=True,
    )
    product_code = models.CharField(max_length=100, null=True, blank=True)
    review_count = models.PositiveIntegerField(null=True, blank=True)
    screen_diagonal = models.CharField(max_length=100, null=True, blank=True)
    display_resolution = models.CharField(max_length=100, null=True, blank=True)
    characteristics = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.full_name or self.product_code or str(self.pk)
