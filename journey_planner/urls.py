from django.urls import path, include
from . import views

urlpatterns = [
    path('journey_planner', views.journey_planner, name='journey_planner'),
    path('register', views.register_request, name='register'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('view_journey', views.view_journey, name='view_journey'),
    path('edit_journey', views.edit_journey, name='edit_journey'),
    path('edit_point',views.edit_point, name='edit_point'),

               ]