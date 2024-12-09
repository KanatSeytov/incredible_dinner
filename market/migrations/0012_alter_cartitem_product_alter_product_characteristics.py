# Generated by Django 5.1.3 on 2024-12-09 12:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0011_product_characteristics_product_min_order_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="market.product",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="characteristics",
            field=models.JSONField(),
        ),
    ]