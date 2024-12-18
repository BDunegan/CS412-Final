# Generated by Django 5.1.2 on 2024-11-21 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('birth_date', models.DateField()),
                ('death_date', models.DateField(blank=True, null=True)),
                ('region', models.TextField()),
                ('field_or_specialty', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.TextField()),
                ('title', models.TextField()),
                ('publication_date', models.DateField()),
                ('theme', models.TextField()),
                ('is_series', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.author')),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.TextField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to='project.book')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('review', models.TextField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.book')),
                ('rating_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.author')),
            ],
            options={
                'unique_together': {('rating_by', 'book')},
            },
        ),
    ]
