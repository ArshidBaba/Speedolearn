# Generated by Django 4.1.7 on 2023-05-22 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0017_course_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='title',
            field=models.CharField(max_length=300),
        ),
    ]
