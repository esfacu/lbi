# Generated by Django 4.2.6 on 2023-11-20 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lbi',
            old_name='number',
            new_name='Number',
        ),
    ]
