# Generated by Django 5.1.2 on 2024-12-06 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_alter_author_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='user',
            new_name='user_id',
        ),
    ]
