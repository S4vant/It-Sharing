# Generated by Django 5.1.3 on 2024-12-05 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_article_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата публликации'),
        ),
    ]
