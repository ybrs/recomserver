# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 13:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interests', '0005_objectwithinterest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objectinterest',
            name='interest',
        ),
        migrations.AddField(
            model_name='objectinterest',
            name='interest_id',
            field=models.BigIntegerField(default=None, null=True),
        ),
    ]