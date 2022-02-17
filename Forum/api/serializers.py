from rest_framework import serializers
from .models import Chapter, Category, Theme, Message
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_staff']


class ChapterSerializer(serializers.ModelSerializer):
    """Сериализатор раздела форума"""
    categories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'description', 'categories']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории форума"""
    chapter = ChapterSerializer()
    themes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'chapter', 'name', 'description', 'themes']


class ChapterRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор раздела форума для получение 1 записи"""
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'description', 'categories']


class CategorySerializerChange(serializers.ModelSerializer):
    """Сериализатор категории обновления/создания/изменения"""

    class Meta:
        model = Category
        fields = ['id', 'chapter', 'name', 'description']


class ThemeSerializer(serializers.ModelSerializer):
    """Сериализатор темы на форуме"""
    category = CategorySerializer()
    messages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Theme
        fields = ['id', 'category', 'name',
                  'status', 'user', 'messages', 'created_at']


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор получения 1 категории форума"""
    chapter = ChapterSerializer()
    themes = ThemeSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'chapter', 'name', 'description', 'themes']


class ThemeSerializerChange(serializers.ModelSerializer):
    """Сериализатор темы на форуме (создание и и обновление)"""

    class Meta:
        model = Theme
        fields = ['id', 'category', 'name',
                  'status', 'user']


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор сообщения на форуме"""

    class Meta:
        model = Message
        fields = ['id', 'user', 'theme', 'content', 'created_at', 'updated_at']


class ThemeRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор получения 1 темы на форуме"""
    category = CategorySerializer()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Theme
        fields = ['id', 'category', 'name',
                  'status', 'user', 'messages', 'created_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    """Сериализатор изменения сообщения на форуме"""

    class Meta:
        model = Message
        fields = ['id', 'user', 'theme', 'content', 'created_at', 'updated_at']

    def validate_theme(self, value):
        """
        Валидация темы, если тема является закрытой
        возникнет исключение ValidationError
        """
        if value.status == False:
            raise serializers.ValidationError(
                "Невозможно создать сообщение в закрытой теме")
        return value
