from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.urls import reverse

sport = 'SP'
politics = 'PL'
IT = 'IT'
economics = 'EC'

TOP = [
    (sport, 'Спорт'),
    (politics, 'Политика'),
    (IT, 'Новости IT'),
    (economics, 'Экономика')
]


class Author(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.name

    def update_rating(self):
        articles_rate = \
            Post.objects.filter(author_id=self.pk).aggregate(sum_articles=Coalesce(Sum('rating_post') * 3, 0))[
                'sum_articles']
        comments_rate = \
            Comment.objects.filter(user_comment_id=self.user).aggregate(
                sum_articles=Coalesce(Sum('rating_comment'), 0))[
                'sum_articles']
        comments_articles_rate = Comment.objects.filter(post_comment__author__users=self.user).aggregate(
            sum_posts=Coalesce(Sum('rating_comment'), 0))['sum_posts']
        self.rating = articles_rate + comments_rate + comments_articles_rate
        self.save()


class Category(models.Model):
    DoesNotExist = None
    objects = None
    name_category = models.CharField(max_length=250, choices=TOP, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name_category


# class SubscribedUsersCategory(models.Model):
#     subscribers = models.ForeignKey(User, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)


article = 'AR'
news = 'NW'
TYPE = [
    (article, 'Article'),
    (news, 'News')
]


class Post(models.Model):
    DoesNotExist = None
    objects = None
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPE, default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    head_name = models.CharField(max_length=250, unique=True)
    text = models.TextField()
    rate = models.IntegerField(default=0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def preview(self):
        preview = f'{self.text[0:124]} ...'
        return preview

    def __str__(self):
        return f'{self.head_name}: {self.text[:40]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])


class PostCategory(models.Model):
    objects = None
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
