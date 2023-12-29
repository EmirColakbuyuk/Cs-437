# secure_api/urls.py
from django.urls import path
from .views import SecureAPI

urlpatterns = [
    path('secure_api/', SecureAPI.as_view(), name='secure-api'),
]
