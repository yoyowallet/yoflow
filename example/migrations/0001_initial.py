# Generated by Django 2.0.1 on 2018-02-10 11:56

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
                ('yoflow_created', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('custom_state_field', models.IntegerField(choices=[(1, 'draft'), (2, 'approved'), (3, 'final')], default=1)),
            ],
            options={
                'permissions': (('draft', 'Can save as draft'), ('approved', 'Can save as approved'), ('final', 'Can save as final')),
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yoflow_created', models.DateTimeField(auto_now_add=True)),
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
