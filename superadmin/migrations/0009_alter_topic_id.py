# Generated by Django 4.1.7 on 2023-04-17 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0008_alter_course_overview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
