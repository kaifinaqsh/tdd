# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-15 21:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_auto_20160315_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='name',
            field=models.TextField(default=b''),
        ),
    ]
