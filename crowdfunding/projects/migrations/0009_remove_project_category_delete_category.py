# Generated by Django 5.1 on 2024-12-01 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_remove_project_location_project_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]