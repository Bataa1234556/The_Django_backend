# Generated by Django 5.0.6 on 2024-05-20 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_models', '0003_group_permission_alter_user_options_user_groups_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='Permission',
        ),
    ]