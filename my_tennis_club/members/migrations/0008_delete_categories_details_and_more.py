# Generated by Django 4.2.3 on 2023-07-23 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_size_productsize_alter_size_productsize_count'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Categories_details',
        ),
        migrations.RemoveField(
            model_name='categories',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='categories',
            name='is_featured',
        ),
    ]
