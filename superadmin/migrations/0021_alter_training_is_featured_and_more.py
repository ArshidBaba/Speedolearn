# Generated by Django 4.1.7 on 2023-05-23 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0020_remove_jobimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='is_featured',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='training',
            name='live_on_website',
            field=models.CharField(max_length=150),
        ),
    ]
