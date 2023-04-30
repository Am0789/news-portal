from django.db import models


reader = 're'
news = 'ne'
post = 'po'

POSITIONS = [
    (reader, 'читатель-пользователь'),
    (news, 'новость'),
    (post, 'статья')
]

class Post(models.Model):  #использовать метод Preview?
    Post_data = models.DateField(auto_now_add=True) #время размещения поста
    Post = models.CharField(max_length=500)
    Post = models.CharField(max_length=2, choices=POSITIONS)#поле выбора ст.новость
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    cost = models.FloatField(default = 0.0)
    Post = models.ForeignKey('Author', on_delete=models.CASCADE)#связь «один ко многим» с моделью Author
    Post = models.ManyToManyField('Category', through = 'PostCategory')


class PostCategory(models.Model):
    Post = models.ForeignKey('Post', on_delete=models.CASCADE)
    PostCategory = models.ForeignKey('Category', on_delete=models.CASCADE)


class Category(models.Model): #категория статьи или новости
    Category = models.CharField(max_length=2, choices=POSITIONS)
    Category = models.CharField(default = ' ')
    Category = models.CharField(max_length=50)

    unique = True


class Comment(models.Model):
    Comment_data = models.DateField(auto_now_add=True) #дата и время создания комментария
    Comment = models.ForeignKey('Post', on_delete=models.CASCADE)#связь «один ко многим» с моделью Post
    Comment = models.ForeignKey('User', on_delete=models.CASCADE)#связь «один ко многим» со встроенной моделью User
    Comment = models.CharField(max_length=500)#текст комментария
#рейтинг комментария


class Author(models.Model):
    Author = models.CharField(max_length=2, choices=POSITIONS)
    name = models.CharField(max_length=50)
    Author = models.OneToOneField('User', on_delete=models.CASCADE)
    Author = models.ForeignKey('Post', on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    #update_rating()

class User(models.Model):
    User = models.CharField(max_length=2, choices=POSITIONS)
    password = models.CharField(('password'), max_length=128)
    last_login = models.DateTimeField(('last login'), blank=True, null=True)

    is_active = True

