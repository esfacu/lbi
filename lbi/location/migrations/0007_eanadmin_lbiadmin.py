# Generated by Django 4.2.6 on 2023-11-29 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0006_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='EanAdmin',
            fields=[
                ('ean_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='location.ean')),
            ],
            bases=('location.ean',),
        ),
        migrations.CreateModel(
            name='LBIAdmin',
            fields=[
                ('lbi_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='location.lbi')),
            ],
            bases=('location.lbi',),
        ),
    ]
