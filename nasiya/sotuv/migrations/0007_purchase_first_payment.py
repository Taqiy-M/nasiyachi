# Generated by Django 4.1.7 on 2023-03-06 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sotuv', '0006_rename_category_purchase_product_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='first_payment',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
