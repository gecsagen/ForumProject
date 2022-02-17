from django.contrib import admin
from .models import Chapter, Category, Theme, Message


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    """Регистрация модели Chapter в админке"""
    list_display = ['id', 'name']
    list_editable = ['name']
    list_display_links = ['id']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Регистрация модели Category в админке"""
    list_display = ['id', 'name', 'chapter']
    list_editable = ['name', 'chapter']
    list_display_links = ['id']


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    """Регистрация модели Theme в админке"""
    list_display = ['id', 'name', 'status', 'category', 'user', 'created_at']
    list_editable = ['name', 'status', 'category']
    list_display_links = ['id']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Регистрация модели Message в админке"""
    list_display = ['id', 'theme', 'user', 'created_at']
    list_editable = ['theme']
    list_display_links = ['id']

