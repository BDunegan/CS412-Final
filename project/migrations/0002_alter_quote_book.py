# Generated by Django 5.1.2 on 2024-11-21 18:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.book'),
        ),
    ]
