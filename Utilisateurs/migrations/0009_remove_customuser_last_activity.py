# Generated by Django 4.2.7 on 2024-01-05 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Utilisateurs', '0008_customuser_last_activity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='last_activity',
        ),
    ]