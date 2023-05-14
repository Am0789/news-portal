# from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.forms import UserCreationForm
from django import forms
# from django.shortcuts import render, redirect
# from django.views import View
# from django.core.mail import mail_admins

article = '01'
news = '02'

TYPE = [
    (article, 'Статья'),
    (news, 'Новость')
]


class Author(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

    def update_rating(self):
        author_posts_rating = Post.objects.filter(author_id=self.pk).aggregate(
            post_rating_sum=Coalesce(Sum('rate') * 3, 0))
        author_comment_rating = Comment.objects.filter(user_id=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rate'), 0))
        author_post_comment_rating = Comment.objects.filter(post__author__user=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rate'), 0))
        print(author_posts_rating)
        print(author_post_comment_rating)
        print(author_post_comment_rating)
        self.rate = author_posts_rating['post_rating_sum'] + author_comment_rating['comments_rating_sum'] / \
                    + author_post_comment_rating['comments_rating_sum']
        self.save()


class Category(models.Model):
    DoesNotExist = None
    objects = None
    name_category = models.CharField(max_length=250, unique=True)
    subscribed_users = models.ManyToManyField(User, through='SubscribedUsersCategory')

    def __str__(self):
        return f'Категория: {self.name_category}'


class SubscribedUsersCategory(models.Model):
    subscribed_users = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    objects = None
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPE, default=article)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    head_name = models.CharField(max_length=250, unique=True)
    article_text = models.TextField()
    rate = models.IntegerField(default=0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def preview(self):
        article_text = self.article_text
        preview = article_text[0:124]
        points = "..."
        return preview + points

    def __str__(self):
        return self.preview()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def __str__(self):
        return self.comment_text


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)
