# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-16 19:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Child',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('custom_state_field', models.IntegerField(choices=[(1, 'draft'), (2, 'approved'), (3, 'final')], default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('state', models.IntegerField(choices=[(1, 'draft'), (2, 'approved'), (3, 'final')], default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='child',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='example.Parent'),
        ),
    ]
