# Generated by Django 5.1.2 on 2024-10-14 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_quote', '0002_alter_quote_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='tags',
            field=models.CharField(max_length=150),
        ),
    ]
