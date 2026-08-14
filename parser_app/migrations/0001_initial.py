import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parser_type', models.CharField(blank=True, choices=[('requests_bs4', 'Requests and BeautifulSoup'), ('selenium', 'Selenium'), ('playwright', 'Playwright')], max_length=32, null=True)),
                ('source_url', models.URLField(blank=True, max_length=2048, null=True)),
                ('full_name', models.CharField(blank=True, max_length=500, null=True)),
                ('color', models.CharField(blank=True, max_length=255, null=True)),
                ('memory_capacity', models.CharField(blank=True, max_length=255, null=True)),
                ('manufacturer', models.CharField(blank=True, max_length=255, null=True)),
                ('regular_price', models.CharField(blank=True, max_length=100, null=True)),
                ('promotional_price', models.CharField(blank=True, max_length=100, null=True)),
                ('image_urls', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(max_length=2048), blank=True, null=True, size=None)),
                ('product_code', models.CharField(blank=True, max_length=100, null=True)),
                ('review_count', models.PositiveIntegerField(blank=True, null=True)),
                ('screen_diagonal', models.CharField(blank=True, max_length=100, null=True)),
                ('display_resolution', models.CharField(blank=True, max_length=100, null=True)),
                ('characteristics', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]
