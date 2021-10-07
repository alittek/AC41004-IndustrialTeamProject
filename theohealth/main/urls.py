from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
        path('', views.index, name="index"),
        path('login/', views.login, name="login"),
        path('overview/<int:pk>', views.OverviewView.as_view(), name="overview"),
        path('athlete/<int:pk>', views.athlete, name="athlete"),
        path('add_athlete/<int:pk>', views.add_athlete, name="add_athlete"),
        path('post_athlete/', views.post_athlete, name="past_athlete"),
        path('request_workout_details/<int:workout_id>', views.request_workout_details, name="request_workout_details"),
        ]
