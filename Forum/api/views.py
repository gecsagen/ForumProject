from .models import Chapter, Category, Theme, Message
from . import serializers
from rest_framework import generics
from rest_framework import permissions
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .permissions import IsOwnerOrStaff
from .paginator import CustomPagination


#  представления для разделов
class ChapterAPIList(generics.ListAPIView):
    """Получение списка разделов"""
    queryset = Chapter.objects.all()
    serializer_class = serializers.ChapterSerializer


class ChapterAPIRetrieve(generics.RetrieveAPIView):
    """Получение 1 раздела"""
    queryset = Chapter.objects.all()
    serializer_class = serializers.ChapterRetrieveSerializer


class ChapterAPICreateUpdateDestroy(mixins.CreateModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin,
                                    generics.GenericAPIView):
    """Изменение и удаление раздела"""
    queryset = Chapter.objects.all()
    serializer_class = serializers.ChapterSerializer
    permission_classes = [permissions.IsAdminUser]

    #  методы для вызова по соответствующим методам http запросов
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


#  представления для категорий
class CategoryAPIList(generics.ListAPIView):
    """Получение списка категорий"""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['chapter']


class CategoryAPIRetrieve(generics.RetrieveAPIView):
    """Получение 1 категории"""
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryRetrieveSerializer


class CategoryAPICreateUpdateDestroy(mixins.CreateModelMixin,
                                     mixins.UpdateModelMixin,
                                     mixins.DestroyModelMixin,
                                     generics.GenericAPIView):
    """Изменение и удаление категории"""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializerChange
    permission_classes = [permissions.IsAdminUser]

    #  методы для вызова по соответствующим методам http запросов
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


#  представления для тем
class ThemeAPIList(generics.ListAPIView):
    """Получение списка тем"""
    queryset = Theme.objects.all()
    serializer_class = serializers.ThemeSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'user', 'status']
    ordering_fields = ['created_at']


class ThemeAPIRetrieve(generics.RetrieveAPIView):
    """Получение 1 темы"""
    queryset = Theme.objects.all()
    serializer_class = serializers.ThemeRetrieveSerializer


class ThemeCreate(generics.CreateAPIView):
    """Создание новой темы"""
    queryset = Theme.objects.all()
    serializer_class = serializers.ThemeSerializerChange
    permission_classes = [permissions.IsAuthenticated]


class ThemeDelete(generics.DestroyAPIView):
    """Удаление темы"""
    queryset = Theme.objects.all()
    serializer_class = serializers.ThemeSerializerChange
    permission_classes = [permissions.IsAdminUser]


class ThemeUpdate(generics.UpdateAPIView):
    """Изменение темы"""
    queryset = Theme.objects.all()
    serializer_class = serializers.ThemeSerializerChange
    permission_classes = [IsOwnerOrStaff]


#  представления для сообщений
class MessageAPIList(generics.ListAPIView):
    """Получение списка сообщений"""
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['theme']


class MessageAPIRetrieve(generics.RetrieveAPIView):
    """Получение 1 сообщения"""
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer


class MessageCreate(generics.CreateAPIView):
    """Создание нового сообщения"""
    queryset = Message.objects.all()
    serializer_class = serializers.MessageCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class MessageDelete(generics.DestroyAPIView):
    """Удаление сообщения"""
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = [permissions.IsAdminUser]


class MessageUpdate(generics.UpdateAPIView):
    """Изменение сообщения"""
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = [IsOwnerOrStaff]
