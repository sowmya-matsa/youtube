# Generated by Django 3.2.5 on 2021-08-05 04:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('entertainment', '0004_rename_user_id_subscriber_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
