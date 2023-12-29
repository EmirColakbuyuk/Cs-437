from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginView, name="login"),
    path('register/', views.registerView, name="register"),
    path('logout/', views.logoutView, name="logout"),
    path('profile/', views.profileView, name="profile"),
    path('changePassword/', views.changePasswordView, name="changePassword"),

]
