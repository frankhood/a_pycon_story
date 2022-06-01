# Generated by Django 3.2.13 on 2022-05-31 14:38

from django.db import migrations, models
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RemoteUser',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('remote_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='Remote ID')),
            ],
            options={
                'verbose_name': 'RemoteUser',
                'verbose_name_plural': 'RemoteUsers',
                'ordering': ['-created'],
                'get_latest_by': '-created',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(blank=True, default='', max_length=255, verbose_name='Name')),
                ('file', models.FileField(upload_to='resources/', verbose_name='File')),
                ('remote_users', models.ManyToManyField(related_name='resources', to='pycon_service.RemoteUser', verbose_name='Remote users')),
            ],
            options={
                'verbose_name': 'RemoteUser',
                'verbose_name_plural': 'RemoteUsers',
                'ordering': ['-created'],
                'get_latest_by': '-created',
                'abstract': False,
            },
        ),
    ]