# Generated by Django 3.2.13 on 2022-06-18 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_rename_data_category_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='musicproduct',
            old_name='track_category',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='musicproduct',
            old_name='all_genre',
            new_name='genre',
        ),
    ]
