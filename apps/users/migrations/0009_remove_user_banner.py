# Generated by Django 5.1.2 on 2024-10-28 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_user_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='banner',
        ),
    ]
