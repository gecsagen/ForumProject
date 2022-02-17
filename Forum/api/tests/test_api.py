"""
Модуль тестирования API приложения
DateForTests - класс с тестовыми данными
ChapterApiTestCase - класс с тестами api разделов форума
CategoryApiTestCase - класс с тестами api категорий форума
ThemeApiTestCase - класс с тестами api тем форума
MessageApiTestCase - класс с тестами api сообщений форума
AuthTokenTest - класс с тестами api авторизации и регистрации по токенам
"""
from datetime import datetime
import json
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from api import models
from api import serializers


class DateForTests(APITestCase):
    """
    Тестовые данные для тестирование api содержаться в этом классе
    Каждый класс-модуль тестирования - наследуется от этого класса
    """

    def setUp(self) -> None:
        """Запускается перед запуском кажого из тестов"""
        #  создаем тестовые юзеры, чтобы не аутентифицироваться
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user_admin = User.objects.create(username='admin', is_staff=True)

        #  создаем тестовые разделы
        self.chapter1 = models.Chapter.objects.create(
            name='chapter 1', description='desc 1')
        self.chapter2 = models.Chapter.objects.create(
            name='chapter 2', description='desc 2')

        #  создаем тестовые категории
        self.category1 = models.Category.objects.create(
            chapter=self.chapter1, name='Category 1', description='desc category 1')
        self.category2 = models.Category.objects.create(
            chapter=self.chapter1, name='Category 2', description='desc category 2')
        self.category3 = models.Category.objects.create(
            chapter=self.chapter2, name='Category 3', description='desc category 3')

        #  создаем тестовые темы
        self.theme1 = models.Theme.objects.create(
            category=self.category1, name='Theme 1', user=self.user1)
        self.theme2 = models.Theme.objects.create(
            category=self.category1, name='Theme 2', status=False, user=self.user1)
        self.theme3 = models.Theme.objects.create(
            category=self.category2, name='Theme 3', user=self.user2)

        #  создаем тестовые сообщения
        self.message1 = models.Message.objects.create(
            user=self.user1, theme=self.theme1, content='content 1')
        self.message2 = models.Message.objects.create(
            user=self.user2, theme=self.theme1, content='content 2')
        self.message3 = models.Message.objects.create(
            user=self.user1, theme=self.theme2, content='content 3')


class ChapterApiTestCase(DateForTests):
    """Модуль тестирования раздела (Chapter)"""

    def setUp(self) -> None:
        return super().setUp()

    def test_get_chapter(self):
        """Тестирование получение 1 раздела"""
        #  создаем url по которому будем делать get запрос
        url = reverse('chapter-detail', args=(self.chapter1.id,))
        #  делаем get запрос с помощью client
        response = self.client.get(url)
        chapter = models.Chapter.objects.get(pk=self.chapter1.id)
        #  передаем список тестовых книг в сереализатор
        serializer_data = serializers.ChapterRetrieveSerializer(chapter).data
        #  сравниваем статус, чтобы он был 200
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        #  проверям равняются ли данные полученные из запроса данным полученым с сереализатора
        self.assertEqual(serializer_data, response.data)

    def test_get_list_chapters(self):
        """Тестирование получения всех разделов"""
        url = reverse('chapter-list')
        response = self.client.get(url)
        chapters = models.Chapter.objects.all()
        serializer_data = serializers.ChapterSerializer(
            chapters, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create_chapter(self):
        """Тестирование создания раздела"""
        self.assertEqual(2, models.Chapter.objects.all().count())
        url = reverse('chapter-create')
        data = {
            'id': 3,
            'name': 'chapter 3',
            'description': 'desc 3',
            'categories': []
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_admin)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, models.Chapter.objects.all().count())

    def test_create_chapter_not_admin(self):
        """Тестирование создания раздела не администратором"""
        self.assertEqual(2, models.Chapter.objects.all().count())
        url = reverse('chapter-create')
        data = {
            'id': 3,
            'name': 'chapter 3',
            'description': 'desc 3',
            'categories': []
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(2, models.Chapter.objects.all().count())

    def test_delete_chapter(self):
        """Удаление раздела"""
        self.assertEqual(2, models.Chapter.objects.all().count())
        url = reverse('chapter-update', args=(self.chapter1.id,))
        self.client.force_login(self.user_admin)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, models.Chapter.objects.all().count())

    def test_delete_chapter_not_admin(self):
        """Тестирование удаления раздела не администратором"""
        self.assertEqual(2, models.Chapter.objects.all().count())
        url = reverse('chapter-update', args=(self.chapter1.id,))
        self.client.force_login(self.user1)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(2, models.Chapter.objects.all().count())

    def test_update_chapter(self):
        """Обновление раздела"""
        url = reverse('chapter-update', args=(self.chapter1.id,))
        self.client.force_login(self.user_admin)
        data = {
            'name': 'chapter 99'
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.chapter1.refresh_from_db()
        self.assertEqual('chapter 99', self.chapter1.name)

    def test_update_chapter_not_admin(self):
        """Тестирование обновления раздела не администратором"""
        url = reverse('chapter-update', args=(self.chapter1.id,))
        self.client.force_login(self.user1)
        data = {
            'name': 'chapter 99'
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.chapter1.refresh_from_db()
        self.assertEqual('chapter 1', self.chapter1.name)


class CategoryApiTestCase(DateForTests):
    """Модуль тестирования категории (Category)"""

    def setUp(self) -> None:
        return super().setUp()

    def test_get_category(self):
        """Тестирование получение 1 категории"""
        url = reverse('category-detail', args=(self.category1.id,))
        response = self.client.get(url)
        category = models.Category.objects.get(pk=self.category1.id)
        serializer_data = serializers.CategoryRetrieveSerializer(category).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_list_categories(self):
        """Тестирование получения всех категорий"""
        url = reverse('category-list')
        response = self.client.get(url)
        categories = models.Category.objects.all()
        serializer_data = serializers.CategorySerializer(
            categories, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create_category(self):
        """Тестирование создания категории"""
        self.assertEqual(3, models.Category.objects.all().count())
        url = reverse('category-create')
        data = {
            'id': 3,
            'chapter': self.chapter2.id,
            'name': 'Category 3',
            'description': 'desc category 3',
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_admin)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, models.Category.objects.all().count())

    def test_create_category_not_admin(self):
        """Тестирование создания категории не администратором"""
        self.assertEqual(3, models.Category.objects.all().count())
        url = reverse('category-create')
        data = {
            'id': 3,
            'chapter': self.chapter2.id,
            'name': 'Category 3',
            'description': 'desc category 3',
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(3, models.Category.objects.all().count())

    def test_delete_category(self):
        """Удаление категории"""
        self.assertEqual(3, models.Category.objects.all().count())
        url = reverse('category-update', args=(self.category1.id,))
        self.client.force_login(self.user_admin)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, models.Category.objects.all().count())

    def test_delete_category_not_admin(self):
        """Тестирование удаления категории не администратором"""
        self.assertEqual(3, models.Category.objects.all().count())
        url = reverse('category-update', args=(self.category1.id,))
        self.client.force_login(self.user1)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(3, models.Category.objects.all().count())

    def test_update_category(self):
        """Обновление категории"""
        url = reverse('category-update', args=(self.category1.id,))
        self.client.force_login(self.user_admin)
        data = {
            'name': 'category 99'
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.category1.refresh_from_db()
        self.assertEqual('category 99', self.category1.name)

    def test_update_category_not_admin(self):
        """Тестирование обновления категории не администратором"""
        url = reverse('category-update', args=(self.category1.id,))
        self.client.force_login(self.user1)
        data = {
            'name': 'category 99'
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.category1.refresh_from_db()
        self.assertEqual('Category 1', self.category1.name)

    def test_filter_category_by_chapter(self):
        """Фильтрация категорий по принадлежности к разделу"""
        url = reverse('category-list')
        response = self.client.get(url, data={'chapter': self.chapter1.id})
        serializer_data = serializers.CategorySerializer(
            [self.category1, self.category2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


class ThemeApiTestCase(DateForTests):
    """Модуль тестирования темы (Theme)"""

    def setUp(self) -> None:
        return super().setUp()

    def test_get_theme(self):
        """Тестирование получение 1 темы"""
        url = reverse('theme-detail', args=(self.theme1.id,))
        response = self.client.get(url)
        theme = models.Theme.objects.get(pk=self.theme1.id)
        serializer_data = serializers.ThemeRetrieveSerializer(theme).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_list_themes(self):
        """Тестирование получения всех тем"""
        url = reverse('theme-list')
        response = self.client.get(url)
        themes = models.Theme.objects.all()
        serializer_data = serializers.ThemeSerializer(
            themes, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data["results"])

    def test_create_theme(self):
        """Тестирование создания темы"""
        self.assertEqual(3, models.Theme.objects.all().count())
        url = reverse('theme-create')
        data = {
            'id': 3,
            'category': self.category1.id,
            'name': 'Theme 3',
            'status': True,
            'user': self.user1.id,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, models.Theme.objects.all().count())

    def test_create_theme_not_authentification(self):
        """
        Тестирование создания темы негативный тест
        Попытка создания темы не аутентифицированным пользователем
        """
        self.assertEqual(3, models.Theme.objects.all().count())
        url = reverse('theme-create')
        data = {
            'id': 3,
            'category': self.category1.id,
            'name': 'Theme 3',
            'status': True,
            'user': self.user1.id,
        }
        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(3, models.Theme.objects.all().count())

    def test_delete_theme(self):
        """Удаление темы"""
        self.assertEqual(3, models.Theme.objects.all().count())
        url = reverse('theme-delete', args=(self.theme1.id,))
        self.client.force_login(self.user_admin)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, models.Theme.objects.all().count())

    def test_delete_theme_not_admin(self):
        """
        Удаление темы негативный тест
        Попытка удалить тему не админом
        """
        self.assertEqual(3, models.Theme.objects.all().count())
        url = reverse('theme-delete', args=(self.theme1.id,))
        self.client.force_login(self.user1)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(3, models.Theme.objects.all().count())

    def test_update_theme(self):
        """Обновление темы"""
        url = reverse('theme-update', args=(self.theme1.id,))
        self.client.force_login(self.user1)
        data = {
            'name': 'Theme 99'
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.theme1.refresh_from_db()
        self.assertEqual('Theme 99', self.theme1.name)

    def test_update_theme_not_owner(self):
        """
        Обновление темы негативный тест
        Попытка изменить тему не создателем темы
        """
        url = reverse('theme-update', args=(self.theme1.id,))
        self.client.force_login(self.user2)
        data = {
            'name': 'Theme 99'
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.theme1.refresh_from_db()
        self.assertEqual('Theme 1', self.theme1.name)

    def test_update_theme_is_admin(self):
        """Тестирование обновления темы админом"""
        url = reverse('theme-update', args=(self.theme1.id,))
        self.client.force_login(self.user_admin)
        data = {
            'name': 'Theme 99'
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.theme1.refresh_from_db()
        self.assertEqual('Theme 99', self.theme1.name)

    def test_filter_themes_by_category(self):
        """Фильтрация тем по принадлежности к категории"""
        url = reverse('theme-list')
        response = self.client.get(url, data={'category': self.category1.id})
        serializer_data = serializers.ThemeSerializer(
            [self.theme1, self.theme2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data["results"])

    def test_filter_themes_by_user(self):
        """Фильтрация тем по принадлежности к пользователю"""
        url = reverse('theme-list')
        response = self.client.get(url, data={'user': self.user1.id})
        serializer_data = serializers.ThemeSerializer(
            [self.theme1, self.theme2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data["results"])

    def test_filter_themes_by_status(self):
        """Фильтрация тем по статусу"""
        url = reverse('theme-list')
        response = self.client.get(url, data={'status': True})
        serializer_data = serializers.ThemeSerializer(
            [self.theme1, self.theme3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data["results"])

    def test_ordring_themes_by_created_at(self):
        """Сортировка тем по дате создания"""
        url = reverse('theme-list')
        response = self.client.get(url, data={'ordering': 'created_at'})
        themes = models.Theme.objects.order_by('created_at')
        serializer_data = serializers.ThemeSerializer(themes, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data["results"])


class MessageApiTestCase(DateForTests):
    """Модуль тестирования сообщении (Message)"""

    def setUp(self) -> None:
        return super().setUp()

    def test_get_mesage(self):
        """Тестирование получение 1 сообщения"""
        url = reverse('message-detail', args=(self.message1.id,))
        response = self.client.get(url)
        message = models.Message.objects.get(pk=self.message1.id)
        serializer_data = serializers.MessageSerializer(message).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_list_messages(self):
        """Тестирование получения всех сообщений"""
        url = reverse('message-list')
        response = self.client.get(url)
        messages = models.Message.objects.all()
        serializer_data = serializers.MessageSerializer(
            messages, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data["results"])

    def test_create_message(self):
        """Тестирование создания сообщения"""
        self.assertEqual(3, models.Message.objects.all().count())
        url = reverse('message-create')
        data = {
            'id': 4,
            'user': self.user1.id,
            'theme': self.theme1.id,
            'content': 'Content 4',
            'created_at': str(datetime.now()),
            'updated_at': str(datetime.now())
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, models.Message.objects.all().count())

    def test_create_message_without_authentification(self):
        """
        Тестирование создания сообщения негативный
        Попытка создания сообщения не аутентифицированным пользователем
        """
        self.assertEqual(3, models.Message.objects.all().count())
        url = reverse('message-create')
        data = {
            'id': 4,
            'user': self.user1.id,
            'theme': self.theme1.id,
            'content': 'Content 4',
            'created_at': str(datetime.now()),
            'updated_at': str(datetime.now())
        }
        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(3, models.Message.objects.all().count())

    def test_create_message_in_close_theme(self):
        """Попытка создать сообщение в закрытой теме"""
        self.assertEqual(3, models.Message.objects.all().count())
        url = reverse('message-create')
        data = {
            'id': 4,
            'user': self.user1.id,
            'theme': self.theme2.id,
            'content': 'Content 4',
            'created_at': str(datetime.now()),
            'updated_at': str(datetime.now())
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(3, models.Message.objects.all().count())

    def test_delete_message(self):
        """Удаление сообщения"""
        self.assertEqual(3, models.Message.objects.all().count())
        url = reverse('message-delete', args=(self.message1.id,))
        self.client.force_login(self.user_admin)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, models.Message.objects.all().count())

    def test_delete_message_not_administrator(self):
        """
        Удаление сообщения негативный тест
        Попытка удалить сообщение не админом
        """
        self.assertEqual(3, models.Message.objects.all().count())
        url = reverse('message-delete', args=(self.message1.id,))
        self.client.force_login(self.user1)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(3, models.Message.objects.all().count())

    def test_update_message(self):
        """Обновление сообщения"""
        url = reverse('message-update', args=(self.message1.id,))
        self.client.force_login(self.user1)
        data = {
            'content': 'Content 99',
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.message1.refresh_from_db()
        self.assertEqual('Content 99', self.message1.content)

    def test_update_message_not_owner(self):
        """
        Обновление сообщения негативный тест
        Попытка изменить сообщение не создателем сообщения
        """
        url = reverse('message-update', args=(self.message1.id,))
        self.client.force_login(self.user2)
        data = {
            'content': 'Content 99'
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.message1.refresh_from_db()
        self.assertEqual('content 1', self.message1.content)

    def test_update_message_is_admin(self):
        """Тестирование обновления сообщения админом"""
        url = reverse('message-update', args=(self.message1.id,))
        self.client.force_login(self.user_admin)
        data = {
            'content': 'Content 99'
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.message1.refresh_from_db()
        self.assertEqual('Content 99', self.message1.content)

    def test_filter_messages_by_theme(self):
        """Фильтрация сообщений по принадлежности к теме"""
        url = reverse('message-list')
        response = self.client.get(url, data={'theme': self.theme1.id})
        messages = models.Message.objects.filter(theme=self.theme1.id)
        serializer_data = serializers.MessageSerializer(
            messages, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data["results"])


class AuthTokenTest(APITestCase):
    """Тестирование аутентификации, регистрации, логаута по токену"""

    def test_auth_registration(self):
        """Тестирование регистрации нового пользователя"""
        url = 'http://127.0.0.1:8000/api/v1/auth/users/'
        data = {
            'username': 'user_1',
            'password': 'UsEr13579U'
        }
        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIsNotNone(response.data)
        self.assertEqual('user_1', response.data.get('username'))

    def test_auth_login(self):
        """Тестирование авторизации нового пользователя"""
        self.test_auth_registration()
        url = reverse('login')
        data = {
            'username': 'user_1',
            'password': 'UsEr13579U'
        }
        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        self.auth_token = response.data.get('auth_token', None)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data)
