# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 13:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interests', '0002_auto_20170223_1306'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InterestUser',
            new_name='InterestObject',
        ),
    ]
