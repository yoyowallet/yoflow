# Generated by Django 2.0.1 on 2018-02-05 11:08

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yoflow_created', models.DateTimeField(auto_now_add=True)),
                ('retailer', models.PositiveIntegerField()),
                ('type', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=256)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={})),
                ('state', models.IntegerField(choices=[(1, 'draft'), (2, 'pending'), (3, 'rejected'), (4, 'approved'), (5, 'deleted')], default=1)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]