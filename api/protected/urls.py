from django.urls import path
from .views import protected_route

urlpatterns = [
    path('protected/', protected_route),
]
