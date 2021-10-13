from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
        path('', views.index, name="index"),
        path('home/', views.home, name="home"),
        path('login/', views.login_form, name="login"),
        path('logout/', views.logout_user, name="logout"),
        path('overview/<int:pk>', views.OverviewView.as_view(), name="overview"),
        path('athlete/<int:pk>', views.athlete, name="athlete"),
        path('add_athlete/<int:pk>', views.add_athlete, name="add_athlete"),
        path('request_workout_details/<int:workout_id>', views.request_workout_details, name="request_workout_details"),
        path('workout', views.workout, name='workout'),
        path('access-restricted', views.access_restricted, name="access-restricted"),
        path('athlete-added', views.athlete_added, name="athlete_added"),
        ]
