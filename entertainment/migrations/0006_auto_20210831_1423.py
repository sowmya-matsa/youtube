# Generated by Django 3.2.5 on 2021-08-31 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entertainment', '0005_subscriber_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='channel',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='user_id',
            new_name='user',
        ),
    ]