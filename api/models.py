from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ("LOCAL", "Local User (Home Mirror)"),
        ("REMOTE", "Remote Cloud User"),
        ("CLIENT", "Client User (Salon)"),
        ("ADMIN", "Salon/Admin Manager"),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="LOCAL")
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    bio = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.username} ({self.role})"
