# Generated by Django 4.1.1 on 2023-03-13 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omorapp', '0002_alter_mail_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='hod',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='mail',
            name='files',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]