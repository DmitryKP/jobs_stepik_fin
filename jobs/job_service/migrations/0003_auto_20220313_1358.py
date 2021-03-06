# Generated by Django 3.2.12 on 2022-03-13 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_service', '0002_auto_20220313_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(null=True, upload_to='company_images'),
        ),
        migrations.AlterField(
            model_name='specialty',
            name='picture',
            field=models.ImageField(null=True, upload_to='speciality_images'),
        ),
    ]
