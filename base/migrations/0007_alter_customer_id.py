# Generated by Django 3.2.20 on 2023-08-09 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20230809_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
