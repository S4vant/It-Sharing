# Generated by Django 5.1.3 on 2024-12-07 17:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_review_finished_time_alter_companies_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='main.companies', verbose_name='Компания'),
        ),
    ]
