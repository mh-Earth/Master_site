from fiverrAppTracker import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # path('', views.save_keystroke , name='save_key_strokes'),
    path('<str:slug>/isPaid', views.is_order_paid , name='is_order_paid'),
    path('<str:slug>/isblocked', views.is_app_blocked , name='is_app_blocked'),
    path('<str:slug>/isDisconnect', views.is_client_disconnected , name='is_client_disconnected'),
]
