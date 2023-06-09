import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category, Author, BaseRegisterForm
from django.views import View
from django.http.response import HttpResponse
from django.utils.translation import gettext as _
from django.utils.translation import activate, get_supported_language_variant
from django.utils import timezone
from django.shortcuts import redirect

import pytz  # импортируем стандартный модуль для работы с часовыми поясами


class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3  # указать количество записей на странице
    logging.error('test_debug')

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        qs = self.get_filter().qs
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('post_list')


class PostDetail(DetailView):
    model = Post
    ordering = '-time_in'
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreateViews(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'news_pos.add_post'
    template_name = 'news_pos.post_create.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news_pos/article/create/':
            post.type = 'AR'
        post.save()
        return super().form_valid(form)


class PostDeleteViews(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    permission_required = 'news_pos.delete_post'
    template_name = 'news_pos.post_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('post_list')


class PostUpdateViews(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'news_pos.change_post'
    template_name = 'news_pos.post_changes_create.html'
    form_class = PostForm
    model = Post

    def get_object(self, **kwargs):
        id_ = self.kwargs.get('pk')
        return Post.objects.get(pk=id_)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'sign.signup.html'
    form_class = UserCreationForm

    def get_object(self, **kwargs):
        username = self.request.user.username
        return User.objects.get(username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assert isinstance(context)
        context['is_not_author'] = not Author.objects.filter(user=self.get_object()).exists()
        context['user_category'] = Category.objects.filter(name_category=self.request.user)
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class SearchPostListView(ListView):
    model = Post
    filter_class = PostFilter
    template_name = 'search.html'
    context_object_name = 'News'
    paginate_by = 10

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.filter_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter_class = PostFilter(self.request.GET, queryset)
        return self.filter_class.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_class'] = self.filter_class
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    massage = 'Вы подписаны на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'massage': massage})


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/News/')


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    message = 'Вы отписались от рассылки новостей категории: '
    return render(request, 'subscribe.html', {'category': category, 'message': message})


@login_required
def news_edit(request, post_id):
    news = get_object_or_404(Post, id=post_id)

    try:
        category_id = news.category.id
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        category = None

    return render(request, 'post_create.html', {'post': news, 'category': category})


class CategoryListView(PostsList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.category = None

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context
