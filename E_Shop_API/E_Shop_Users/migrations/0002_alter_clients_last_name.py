# Generated by Django 4.2.3 on 2023-07-06 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('E_Shop_Users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
