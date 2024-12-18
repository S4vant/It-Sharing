# Generated by Django 5.1.3 on 2024-12-08 09:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_companies_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companies',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='static/main/img/companiesimg', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='review',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='main.order', verbose_name='Заказ'),
        ),
    ]
