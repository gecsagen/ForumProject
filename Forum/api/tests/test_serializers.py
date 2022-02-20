"""
Модуль тестирование серриализаторов
TestSerializers - класс содержит тесты сериализаторов
"""

from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Category, Chapter, Theme, Message, MessageRelation
from api import serializers
from django.contrib.auth.models import User
from api import serializers


class TestSerializers(TestCase):
    """Тестирование сереализаторов"""

    def setUp(self) -> None:
        #  создаем тестовые юзеры
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user3 = User.objects.create(username='user3')

        #  создаем тестовые разделы
        self.chapter1 = Chapter.objects.create(
            name='chapter 1', description='desc 1')
        self.chapter2 = Chapter.objects.create(
            name='chapter 2', description='desc 2')
        self.chapter3 = Chapter.objects.create(
            name='chapter 3', description='desc 3')

        #  создаем тестовые категории
        self.category1 = Category.objects.create(
            chapter=self.chapter1, name='category 1', description='decs category 1')
        self.category2 = Category.objects.create(
            chapter=self.chapter1, name='category 2', description='decs category 2')
        self.category3 = Category.objects.create(
            chapter=self.chapter1, name='category 3', description='decs category 3')

        #  создаем тестовые темы
        self.theme1 = Theme.objects.create(
            category=self.category1, name='theme 1', user=self.user1)
        self.theme2 = Theme.objects.create(
            category=self.category1, name='theme 2', status=False, user=self.user2)
        self.theme3 = Theme.objects.create(
            category=self.category1, name='theme 3', user=self.user3)

        #  создаем сообщения для тем
        self.message1 = Message.objects.create(
            user=self.user1, theme=self.theme1, content='Content 1')
        self.message2 = Message.objects.create(
            user=self.user2, theme=self.theme1, content='Content 2')
        self.message3 = Message.objects.create(
            user=self.user3, theme=self.theme1, content='Content 3')

        #  создаем тестовые оценки
        self.grade1 = MessageRelation.objects.create(
            user=self.user1, message=self.message1, like=True)
        self.grade2 = MessageRelation.objects.create(
            user=self.user2, message=self.message1, like=True)
        self.grade3 = MessageRelation.objects.create(
            user=self.user3, message=self.message1, like=True)

    def test_user_serializer(self):
        """Сереализация пользователя"""
        user = User.objects.get(pk=self.user1.id)
        data = serializers.UserSerializer(user).data
        expected_data = {
            'id': self.user1.id,
            'username': 'user1',
            'first_name': '',
            'last_name': '',
            'is_staff': False
        }
        self.assertEqual(expected_data, data)

    def test_chapter_serializer(self):
        """Сереализация раздела (chapter)"""
        chapters = Chapter.objects.all()
        data = serializers.ChapterSerializer(chapters, many=True).data

        expected_data = [
            {
                'id': self.chapter1.id,
                'name': 'chapter 1',
                'description': 'desc 1',
                'categories': [1, 2, 3]
            },
            {
                'id': self.chapter2.id,
                'name': 'chapter 2',
                'description': 'desc 2',
                'categories': []
            },
            {
                'id': self.chapter3.id,
                'name': 'chapter 3',
                'description': 'desc 3',
                'categories': []
            },
        ]
        self.assertEqual(expected_data, data)

    def test_chapter_retrieve_serializer(self):
        """Сереализация раздела для получения 1 раздела"""
        chapter = Chapter.objects.get(pk=self.chapter1.id)
        data = serializers.ChapterRetrieveSerializer(chapter).data

        expected_data = {
            'id': self.chapter1.id,
            'name': 'chapter 1',
            'description': 'desc 1',
            'categories': serializers.CategorySerializer(Category.objects.all(), many=True).data,
        }
        self.assertEqual(expected_data, data)

    def test_category_serializer(self):
        """Сереализация категории (Category)"""
        data = serializers.CategorySerializer(self.category1).data

        expected_data = {
            'id': self.category1.id,
            'chapter': serializers.ChapterSerializer(self.chapter1).data,
            'name': 'category 1',
            'description': 'decs category 1',
            'themes': [1, 2, 3]
        }
        self.assertEqual(expected_data, data)

    def test_category_retrieve_serializer(self):
        """Сереализация получения 1 категории"""
        data = serializers.CategoryRetrieveSerializer(self.category1).data

        expected_data = {
            'id': self.category1.id,
            'chapter': serializers.ChapterSerializer(self.chapter1).data,
            'name': 'category 1',
            'description': 'decs category 1',
            'themes': serializers.ThemeSerializer(Theme.objects.all(), many=True).data
        }
        self.assertEqual(expected_data, data)

    def test_category_change_serializer(self):
        """Сереализация иземенения категории (Category)"""
        data = serializers.CategorySerializerChange(self.category1).data

        expected_data = {
            'id': self.category1.id,
            'chapter': self.chapter1.id,
            'name': 'category 1',
            'description': 'decs category 1',
        }
        self.assertEqual(expected_data, data)

    def test_theme_serializer(self):
        """Сереализация темы (Theme)"""
        data = serializers.ThemeSerializer(self.theme1).data
        expected_data = {
            'id': self.theme1.id,
            'category': serializers.CategorySerializer(self.category1).data,
            'name': 'theme 1',
            'status': True,
            'user': self.user1.id,
            'messages': [1, 2, 3],
            'created_at': data.get('created_at')
        }
        self.assertEqual(expected_data, data)

    def test_theme_change_serializer(self):
        """Сереализация иземенения темы (Theme)"""
        data = serializers.ThemeSerializerChange(self.theme1).data
        expected_data = {
            'id': self.theme1.id,
            'category': self.category1.id,
            'name': 'theme 1',
            'status': True,
            'user': self.user1.id,
        }
        self.assertEqual(expected_data, data)

    def test_theme_retrieve_serializer(self):
        """Сереализация получения 1 темы"""
        data = serializers.ThemeRetrieveSerializer(self.theme1).data
        expected_data = {
            'id': self.theme1.id,
            'category': serializers.CategorySerializer(self.category1).data,
            'name': 'theme 1',
            'status': True,
            'user': self.user1.id,
            'messages': serializers.MessageSerializer(Message.objects.all(), many=True).data,
            'created_at': data.get('created_at')
        }
        self.assertEqual(expected_data, data)

    def test_message_serializer(self):
        """Сереализация сообщения на форуме"""
        data = serializers.MessageSerializer(self.message1).data
        expected_data = {
            'id': self.message1.id,
            'user': self.user1.id,
            'theme': self.theme1.id,
            'content': 'Content 1',
            'likes_count': 3,
            'created_at': data.get('created_at'),
            'updated_at': data.get('updated_at')
        }
        self.assertEqual(expected_data, data)

    def test_message_relation_serializer(self):
        """Сериализация оценки"""
        data = serializers.MessageRelationSerializer(self.grade1).data
        expected_data = {
            'id': self.grade1.id,
            'user': self.user1.id,
            'message': self.message1.id,
            'like': True
        }
        self.assertEqual(expected_data, data)
