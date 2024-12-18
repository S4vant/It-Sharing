# Generated by Django 5.1.3 on 2024-12-08 06:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_companies_representative'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companies',
            name='representative',
        ),
        migrations.AddField(
            model_name='companies',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_companies', to=settings.AUTH_USER_MODEL, verbose_name='Создатель компании'),
        ),
    ]
