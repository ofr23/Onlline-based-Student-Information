# Generated by Django 4.1.1 on 2023-03-25 16:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('omorapp', '0011_mail_mailid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='mailId',
            field=models.UUIDField(default=uuid.uuid4, null=True, unique=True),
        ),
    ]
