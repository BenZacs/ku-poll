# Generated by Django 2.2.7 on 2020-09-20 12:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 30, 12, 22, 14, 477833, tzinfo=utc), verbose_name='ending date'),
        ),
    ]
