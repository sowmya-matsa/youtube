# Generated by Django 3.2.5 on 2021-07-30 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entertainment', '0005_auto_20210730_1103'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='user_id',
        ),
    ]
