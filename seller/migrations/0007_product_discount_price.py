# Generated by Django 2.1.4 on 2020-05-29 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0006_product_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.FloatField(default=0),
        ),
    ]
