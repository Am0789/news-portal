# Generated by Django 4.2 on 2023-05-02 09:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Post_data', models.DateField(auto_now_add=True)),
                ('post_name', models.CharField(default='noname', max_length=255)),
                ('post_rating', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(default='user', max_length=30)),
                ('user', models.CharField(choices=[('re', 'читатель-пользователь'), ('ne', 'новость'), ('po', 'статья')], max_length=2)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post')),
                ('PostCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='Post',
            field=models.ManyToManyField(through='news.PostCategory', to='news.category'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_data', models.DateField(auto_now_add=True)),
                ('comm_text', models.CharField(max_length=500)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.user')),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(default='noname', max_length=30)),
                ('user_rating', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
