# Generated by Django 3.2.13 on 2022-08-06 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_alter_playlist_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='img_playlist/', verbose_name='Image for playlist'),
        ),
    ]
