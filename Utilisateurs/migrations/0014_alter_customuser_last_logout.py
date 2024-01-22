# Generated by Django 4.2.7 on 2024-01-08 11:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Utilisateurs', '0013_customuser_last_logout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='last_logout',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
