# Generated by Django 3.2.13 on 2022-06-30 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_musicproduct_all_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='playlist',
            field=models.ManyToManyField(blank=True, to='core.Playlist', verbose_name='All playlists'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Customer website+', to='core.customer', verbose_name='Customer'),
        ),
    ]
