# Generated by Django 4.2.7 on 2024-01-09 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Utilisateurs', '0022_remove_blogpost_show_full_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
