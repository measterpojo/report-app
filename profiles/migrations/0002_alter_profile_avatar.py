# Generated by Django 3.2.8 on 2021-10-15 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='no_picture.png', upload_to='avatars'),
        ),
    ]