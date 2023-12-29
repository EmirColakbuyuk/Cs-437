from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('latest/', views.latest, name="latest"),
    path('sport/', views.sport, name="sport"),
    path('economy/', views.economy, name="economy"),
    path('magazine/', views.magazine, name="magazine"),
    path('newsDetail/', views.newsDetail, name="newsDetail"),
    path('apiSearch', views.apiSearch, name="apiSearch"),
    path('titleSearch/', views.titleSearch, name="titleSearch"),
    path('deleteComment/<int:comment_id>/', views.deleteComment, name='deleteComment'),


]
#