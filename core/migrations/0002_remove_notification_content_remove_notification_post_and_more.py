# Generated by Django 5.0.6 on 2024-06-15 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='content',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='post',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='user_profile',
        ),
    ]