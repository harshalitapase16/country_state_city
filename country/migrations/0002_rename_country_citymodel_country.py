# Generated by Django 4.2.6 on 2024-07-18 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='citymodel',
            old_name='Country',
            new_name='country',
        ),
    ]
