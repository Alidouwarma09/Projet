# Generated by Django 5.0.1 on 2024-01-29 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Utilisateurs', '0026_rename_image_blogpost_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog_images/')),
            ],
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='images',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='blog_posts', to='Utilisateurs.blogimage'),
        ),
    ]