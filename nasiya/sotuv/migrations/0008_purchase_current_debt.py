# Generated by Django 4.1.7 on 2023-03-07 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sotuv', '0007_purchase_first_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='current_debt',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
