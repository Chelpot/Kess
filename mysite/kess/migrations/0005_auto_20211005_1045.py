# Generated by Django 3.2.7 on 2021-10-05 08:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kess', '0004_auto_20211005_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kess',
            name='foundList',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 5, 10, 45, 3, 994361)),
        ),
    ]
