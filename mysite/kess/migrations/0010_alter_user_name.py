# Generated by Django 3.2.7 on 2021-10-07 07:32

from django.db import migrations, models
import kess.models


class Migration(migrations.Migration):

    dependencies = [
        ('kess', '0009_auto_20211006_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=32, validators=[kess.models.is_ascii]),
        ),
    ]
