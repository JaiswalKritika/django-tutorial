# Generated by Django 4.2.3 on 2023-07-21 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Size Title')),
                ('slug', models.SlugField(max_length=55, verbose_name='Size Slug')),
                ('productSize_count', models.CharField(max_length=50, verbose_name='productColor count')),
            ],
        ),
        migrations.RemoveField(
            model_name='products',
            name='color_name',
        ),
        migrations.AddField(
            model_name='products',
            name='color',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='members.colors', verbose_name='Product Color'),
        ),
        migrations.AddField(
            model_name='products',
            name='fabric',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='members.fabrics', verbose_name='Product Fabric'),
        ),
        migrations.AddField(
            model_name='products',
            name='size',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='members.size', verbose_name='Product size'),
        ),
    ]