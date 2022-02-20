from django.db import models
from django.contrib.auth.models import User


class Chapter(models.Model):
    """Раздел форума"""
    name = models.CharField(max_length=500, verbose_name='Имя раздела')
    description = models.TextField(blank=True, verbose_name='Описание раздела')

    def __str__(self):
        return f'{self.id} - Раздел - {self.name}'

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class Category(models.Model):
    """Категория форума"""
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, related_name='categories', verbose_name='Раздел')
    name = models.CharField(max_length=500, verbose_name='Имя категории')
    description = models.TextField(
        blank=True, verbose_name='Описание категории')

    def __str__(self):
        return f'{self.id} - Категория - {self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Theme(models.Model):
    """Тема"""
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='themes', verbose_name='Категория')
    name = models.CharField(max_length=500, verbose_name='Название темы')
    status = models.BooleanField(default=True, verbose_name='Закрыта/открыта')
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='themes', verbose_name='Создатель темы')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.id} - Тема - {self.name}'

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class Message(models.Model):
    """Сообщение в теме"""
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='messages', verbose_name='Пользователь')
    theme = models.ForeignKey(
        Theme, on_delete=models.CASCADE, related_name='messages', verbose_name='Тема')
    content = models.TextField(verbose_name='Текст сообщения')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'{self.id} - Пост - {self.content[:10]}'

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MessageRelation(models.Model):
    """Модель оценок"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='users', verbose_name='Пользователь')
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    like = models.BooleanField(default=False, verbose_name='Лайк')

    def __str__(self):
        return f"{self.user.username}_{self.like}"

    class Meta:
        verbose_name = 'Relation'
        verbose_name_plural = 'Relations'
