# Generated by Django 4.2.3 on 2023-07-26 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_delete_categories_details_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='status',
            field=models.CharField(choices=[('PUBLISH', 'PUBLISH'), ('DRAFT', 'DRAFT')], default='', max_length=160),
        ),
    ]
