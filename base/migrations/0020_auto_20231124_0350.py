# Generated by Django 3.2.21 on 2023-11-24 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_orderitems_total_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitems',
            name='total_amount',
        ),
        migrations.AddField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
