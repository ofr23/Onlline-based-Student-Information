# Generated by Django 4.1.1 on 2023-03-14 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omorapp', '0003_teacher_hod_alter_mail_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalevaluation',
            name='cgpa',
            field=models.DecimalField(blank=True, decimal_places=2, default='0.0', max_digits=4),
        ),
    ]
