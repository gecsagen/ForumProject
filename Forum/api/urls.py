from django.urls import path, include
from api import views

urlpatterns = [
    #  urls для авторизации по токену
    path('auth/', include('djoser.urls')),
    path('auth-token/', include('djoser.urls.authtoken')),

    #  urls для разделов
    path('chapters/', views.ChapterAPIList.as_view(), name='chapter-list'),
    path('chapters/<int:pk>/', views.ChapterAPIRetrieve.as_view(),
         name='chapter-detail'),
    path('chapters/update/<int:pk>/',
         views.ChapterAPICreateUpdateDestroy.as_view(), name='chapter-update'),
    path('chapters/create/', views.ChapterAPICreateUpdateDestroy.as_view(),
         name='chapter-create'),

    # urls для разделов
    path('categories/', views.CategoryAPIList.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryAPIRetrieve.as_view(),
         name='category-detail'),
    path('categories/update/<int:pk>/',
         views.CategoryAPICreateUpdateDestroy.as_view(), name='category-update'),
    path('categories/create/',
         views.CategoryAPICreateUpdateDestroy.as_view(), name='category-create'),

    #  urls для тем
    path('themes/', views.ThemeAPIList.as_view(), name='theme-list'),
    path('themes/<int:pk>/', views.ThemeAPIRetrieve.as_view(),
         name='theme-detail'),
    path('themes/update/<int:pk>/',
         views.ThemeUpdate.as_view(), name='theme-update'),
    path('themes/create/',
         views.ThemeCreate.as_view(), name='theme-create'),
    path('themes/delete/<int:pk>/',
         views.ThemeDelete.as_view(), name='theme-delete'),

    #  urls для сообщений
    path('messages/', views.MessageAPIList.as_view(), name='message-list'),
    path('messages/<int:pk>/', views.MessageAPIRetrieve.as_view(),
         name='message-detail'),
    path('messages/update/<int:pk>/',
         views.MessageUpdate.as_view(), name='message-update'),
    path('messages/create/',
         views.MessageCreate.as_view(), name='message-create'),
    path('messages/delete/<int:pk>/',
         views.MessageDelete.as_view(), name='message-delete'),
]
