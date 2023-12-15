from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('latest/', views.latest, name="latest"),
    path('sport/', views.sport, name="sport"),
    path('economy/', views.economy, name="economy"),
    path('magazine/', views.magazine, name="magazine"),
    path('search/', views.search, name="search"),

]