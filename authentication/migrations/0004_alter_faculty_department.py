# Generated by Django 5.1.3 on 2024-11-15 06:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic_management', '0001_initial'),
        ('authentication', '0003_verification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic_management.department'),
        ),
    ]