# Generated by Django 4.1.7 on 2023-04-08 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sotuv', '0009_purchase_next_payment_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='not_completed',
        ),
        migrations.AddField(
            model_name='purchase',
            name='completed',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
