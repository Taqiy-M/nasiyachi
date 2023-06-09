# Generated by Django 4.1.7 on 2023-04-13 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sotuv', '0010_remove_purchase_not_completed_purchase_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='last_payment_date',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='purchase',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='sotuv.purchase'),
        ),
    ]
