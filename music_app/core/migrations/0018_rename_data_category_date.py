# Generated by Django 3.2.13 on 2022-06-16 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_category_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='data',
            new_name='date',
        ),
    ]