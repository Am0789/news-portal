# Generated by Django 4.2 on 2023-04-30 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_user_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='position',
        ),
        migrations.RemoveField(
            model_name='user',
            name='position',
        ),
        migrations.AddField(
            model_name='user',
            name='User',
            field=models.CharField(choices=[('re', 'читатель-пользователь'), ('ne', 'новость'), ('po', 'статья')], default=1, max_length=2),
            preserve_default=False,
        ),
    ]
