# Generated by Django 4.1.7 on 2023-06-07 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_alter_teacher_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='campus',
            field=models.CharField(choices=[('Amritsar', 'Amritsar'), ('Mohali Campus 1 ', 'Mohali Campus 1 '), ('Hoshiarpur', 'Hoshiarpur'), ('Mohali Campus 2 ', 'Mohali Campus 2 ')], default='', max_length=40),
            preserve_default=False,
        ),
    ]