# Generated by Django 5.1.2 on 2024-10-28 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='banners/'),
        ),
    ]