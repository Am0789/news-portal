from django.forms import ModelForm, ModelChoiceField, CharField, Select, ModelMultipleChoiceField, Textarea
from .models import Post, Author, Category, TYPE
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(ModelForm):
    author = ModelChoiceField(queryset=Author.objects.all(), label='Автор:')
    post_or_news = CharField(label='Статья или Новость:', widget=Select(choices=TYPE))
    category = ModelMultipleChoiceField(label='Категория', queryset=Category.objects.all())
    title = CharField(label='Заголовок', max_length=255)
    text = CharField(label='Текст статьи', widget=Textarea())

    class Meta:
        model = Post
        fields = [
            'author', 'category', 'title', 'text', 'post_or_news'
        ]


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
