# Generated by Django 2.1.4 on 2020-05-14 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0003_remove_product_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(to='seller.Tag'),
        ),
    ]
