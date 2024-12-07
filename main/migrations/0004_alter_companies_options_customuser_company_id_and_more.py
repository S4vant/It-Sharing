# Generated by Django 5.1.3 on 2024-12-05 20:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_companies'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companies',
            options={'ordering': ['id'], 'verbose_name': 'Компания', 'verbose_name_plural': 'IT компания'},
        ),
        migrations.AddField(
            model_name='customuser',
            name='company_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.companies'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_company',
            field=models.BooleanField(default=False),
        ),
    ]
