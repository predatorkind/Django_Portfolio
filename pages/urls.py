from django.urls import path, include
from . import views

urlpatterns = [path('about_me', views.about_me, name='about_me'),
               path('pool', views.pool, name='pool'),
               path('', views.links, name='links'),
               ]