# Generated by Django 3.2.12 on 2022-03-13 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job_service', '0003_auto_20220313_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL),
        ),
    ]
