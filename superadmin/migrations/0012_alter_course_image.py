# Generated by Django 4.1.7 on 2023-05-02 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0011_alter_course_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
