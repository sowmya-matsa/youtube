# Generated by Django 3.2.5 on 2021-07-22 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entertainment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='channel',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='entertainment.channel'),
        ),
    ]
