from django.urls import path

from . import views

app_name = 'playground'
urlpatterns = [
        path('', views.index, name="index"),
        path('test/', views.test, name="test"),
        path('test1/', views.test1, name="test1"),
        ]
