# Generated by Django 4.2.7 on 2024-01-09 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Utilisateurs', '0017_message_is_read'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='unread_messages',
            new_name='unread_messages_count',
        ),
    ]
