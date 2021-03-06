# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectInterestHash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.BigIntegerField(default=None, null=True)),
                ('phash', models.BigIntegerField()),
                ('phash_hex', models.TextField(default=None, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='userinteresthash',
            name='user',
        ),
        migrations.RemoveField(
            model_name='interestuser',
            name='user',
        ),
        migrations.AddField(
            model_name='interestuser',
            name='object_id',
            field=models.BigIntegerField(default=None, null=True),
        ),
        migrations.DeleteModel(
            name='UserInterestHash',
        ),
    ]
