# Generated by Django 4.1.7 on 2023-03-27 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0003_rename_image_vendor_logo_vendor_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=300)),
                ('answer', models.TextField(max_length=300)),
            ],
        ),
    ]
