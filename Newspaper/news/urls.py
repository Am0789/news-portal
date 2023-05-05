from django.urls import path
from .views import PostDetail, PostsList, PostCreateViews, PostUpdateViews, PostDeleteViews

urlpatterns = [
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('', PostsList.as_view()),
    path('create/', PostCreateViews.as_view(), name='post_create'),
    path('create/<int:pk>', PostUpdateViews.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteViews.as_view(), name='post_delete')
    ]