# Generated by Django 3.2.7 on 2021-10-07 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kess', '0010_alter_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.CharField(max_length=1)),
                ('name', models.CharField(max_length=200)),
                ('action', models.CharField(max_length=200)),
                ('time', models.CharField(max_length=200)),
            ],
        ),
    ]
