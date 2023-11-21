# Generated by Django 4.2.6 on 2023-11-21 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_rename_number_lbi_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ean',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ean_code', models.CharField(max_length=13)),
                ('lbi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.lbi')),
            ],
        ),
    ]