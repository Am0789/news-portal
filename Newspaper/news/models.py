from django.db import models
from django.contrib.auth.models import User


reader = 're'
news = 'ne'
post = 'po'

POSITIONS = [
    (reader, 'читатель-пользователь'),
    (news, 'новость'),
    (post, 'статья')
]

class Post(models.Model):
    Post_data = models.DateField(auto_now_add=True) #время размещения поста
    post_name = models.CharField(max_length=255, default='noname')
    Post = models.CharField(max_length=2, choices=POSITIONS)#поле выбора ст.новость
    post_rating = models.IntegerField(default=0)
    Post = models.ForeignKey('Author', on_delete=models.CASCADE)#связь «один ко многим» с моделью Author
    Post = models.ManyToManyField('Category', through = 'PostCategory')


class PostCategory(models.Model):
    Post = models.ForeignKey('Post', on_delete=models.CASCADE)
    PostCategory = models.ForeignKey('Category', on_delete=models.CASCADE)


class Category(models.Model): #категория статьи или новости
        name = models.CharField(max_length=200, unique=True)


class Comment(models.Model):
    comment_data = models.DateField(auto_now_add=True) #дата и время создания комментария
    comment = models.ForeignKey('Post', on_delete=models.CASCADE)#связь «один ко многим» с моделью Post
    comment = models.ForeignKey('User', on_delete=models.CASCADE)#связь «один ко многим» со встроенной моделью User
    comm_text = models.CharField(max_length=500)#текст комментария
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class Author(models.Model):
    user_name = models.CharField(max_length=30, default='noname')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = self.post.post_rating * 3
        user_rating = self.user_rating
        summ = int(post_rating +com_rating + user_rating)
        return summ


class User(models.Model):
    user_name = models.CharField(max_length=30, default='user')
    user = models.CharField(max_length=2, choices=POSITIONS)
    password = models.CharField(('password'), max_length=128)
    last_login = models.DateTimeField(('last login'), blank=True, null=True)

    is_active = True

