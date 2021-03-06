# Generated by Django 2.1.5 on 2019-04-14 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_id', models.CharField(max_length=10)),
                ('show_title', models.CharField(max_length=100)),
                ('show_genre', models.CharField(max_length=100)),
                ('show_plot', models.CharField(max_length=100)),
                ('show_link', models.CharField(max_length=100)),
                ('show_rating', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Show_Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('show_id', models.CharField(max_length=100)),
                ('rating', models.IntegerField()),
            ],
        ),
    ]
