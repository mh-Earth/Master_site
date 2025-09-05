from key_logger import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.save_keystroke , name='save_key_strokes'),
    # path('/api/logger', views.key_logger , name='key_logger'),
    # path('api/logger/key', views.key_logger , name='key_logger'),
]
