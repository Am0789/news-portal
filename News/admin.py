from django.contrib import admin
from .models import *


# class PostAdmin(admin.ModelAdmin):
#     list_display = ('type', 'category')
#     search_fields = ('head_name', 'category__name')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('rate', 'user')


# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name_category', 'subscribers')
#     search_fields = 'name_category'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('rating', 'user')


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')


# admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Author, AuthorAdmin)
# admin.site.register(Category, CategoryAdmin)
