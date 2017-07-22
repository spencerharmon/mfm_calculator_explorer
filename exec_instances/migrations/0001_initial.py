# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-04 23:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AEPS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aeps', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ExecInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('title', models.CharField(default='[no title]', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='aeps',
            name='exec_instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exec_instances.ExecInstance'),
        ),
    ]