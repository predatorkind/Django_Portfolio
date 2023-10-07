from django.urls import path, include
from . import views

urlpatterns = [
    path('journey_planner', views.journey_planner, name='journey_planner'),
    path('register', views.register_request, name='register')
               ]