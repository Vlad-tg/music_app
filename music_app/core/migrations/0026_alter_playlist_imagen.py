# Generated by Django 3.2.13 on 2022-06-30 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_playlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='imagen',
            field=models.ImageField(default='img_playlist/music_icon.svg', upload_to='img_playlist/', verbose_name='Image for playlist'),
        ),
    ]
