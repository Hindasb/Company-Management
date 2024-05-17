# Generated by Django 5.0.6 on 2024-05-16 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='permission',
            field=models.ManyToManyField(to='auth.permission'),
        ),
        migrations.DeleteModel(
            name='CustomPermission',
        ),
    ]