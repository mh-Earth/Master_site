from key_logger import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # path('api/logger', views.key_logger , name='key_logger')
    path('', views.key_logger , name='')
]
