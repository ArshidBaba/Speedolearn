# Generated by Django 4.1.7 on 2023-06-03 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0021_alter_training_is_featured_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prerequisites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prerequisite', models.TextField(max_length=500)),
            ],
        ),
    ]