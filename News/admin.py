from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


class CommentAdmin(admin.ModelAdmin):
    list_display = ('rating', 'user')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('rating', 'user')


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post


admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Author, AuthorAdmin)


admin.site.register(Post)
admin.site.register(Category)
