# Generated by Django 3.2.13 on 2022-06-28 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='musicproduct',
            name='all_like',
            field=models.ManyToManyField(blank=True, null=True, to='core.Like', verbose_name='All like'),
        ),
    ]
