# Generated by Django 3.2.13 on 2022-04-26 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_musicproduct_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='musicproduct',
            name='track_url',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Url track'),
        ),
    ]