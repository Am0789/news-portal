from allauth.account.views import LoginView, LogoutView
from django.urls import path

from .views import PostDetail, PostsList, PostCreateViews, PostUpdateViews, PostDeleteViews, upgrade_me, \
   BaseRegisterView, SearchPostListView

urlpatterns = [
   path('', PostsList.as_view()),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreateViews.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdateViews.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDeleteViews.as_view(), name='post_delete'),
   path('article/create/', PostCreateViews.as_view()),
   path('article/<int:pk>/update/', PostUpdateViews.as_view()),
   path('article/<int:pk>/delete/', PostDeleteViews.as_view()),
   path('signup/', BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),
   path('search/', SearchPostListView.as_view()),
   path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
   path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
   path('upgrade/', upgrade_me, name='upgrade'),
]
