# Generated by Django 2.1.2 on 2018-10-16 23:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sluck_api', '0002_auto_20181015_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token_updated_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 16, 23, 42, 18, 234060, tzinfo=utc)),
        ),
    ]
