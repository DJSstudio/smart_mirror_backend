from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('protected/', views.protected_view),
    path('auth/me/', views.me, name='me'),
    path('auth/me/update/', views.update_me),

    # add other endpoints...
]
