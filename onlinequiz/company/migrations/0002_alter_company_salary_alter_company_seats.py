# Generated by Django 4.1.7 on 2023-05-10 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='salary',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='company',
            name='seats',
            field=models.IntegerField(),
        ),
    ]
