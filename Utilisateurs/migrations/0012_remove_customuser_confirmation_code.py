# Generated by Django 4.2.7 on 2024-01-08 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Utilisateurs', '0011_customuser_confirmation_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='confirmation_code',
        ),
    ]
