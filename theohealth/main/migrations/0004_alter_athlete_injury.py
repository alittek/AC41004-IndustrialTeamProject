# Generated by Django 3.2.7 on 2021-10-09 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_merge_20211008_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athlete',
            name='injury',
            field=models.CharField(default='', max_length=256),
        ),
    ]
