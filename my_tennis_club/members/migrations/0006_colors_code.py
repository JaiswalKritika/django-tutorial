# Generated by Django 4.2.3 on 2023-07-23 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_tag_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='colors',
            name='code',
            field=models.CharField(default='', max_length=70),
        ),
    ]
