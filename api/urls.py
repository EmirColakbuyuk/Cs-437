from django.urls import path
from .views import SecureAPI, PingAPI

urlpatterns = [
    path('secure_api/', SecureAPI.as_view(), name='secure-api'),
    path('ping/', PingAPI.as_view(), name='ping-api')
]