# Generated by Django 3.1.4 on 2020-12-13 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_auto_20201210_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='participants',
            field=models.ManyToManyField(null=True, related_name='course_participants', to='main_app.User'),
        ),
    ]
