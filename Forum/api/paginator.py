from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Пагинатор для тем и сообщений"""
    page_size = 15
    max_page_size = 200
    last_page_strings = ('the_end',)