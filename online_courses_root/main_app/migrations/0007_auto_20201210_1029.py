# Generated by Django 3.1.4 on 2020-12-10 10:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20201210_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mark',
            name='mark',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
