# Generated by Django 2.1.5 on 2019-04-15 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20190414_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie_rating',
            name='rating',
            field=models.FloatField(),
        ),
    ]
