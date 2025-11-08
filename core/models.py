from django.db import models
from django.conf import settings  # <-- Use this instead of importing User directly


class MirrorDevice(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    location_description = models.CharField(max_length=255, null=True, blank=True)

    # HOME | CLOUD | SALON (mirror mode)
    mode = models.CharField(max_length=20)

    # Link to the custom user model
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_devices"
    )

    def __str__(self):
        return f"MirrorDevice {self.device_id} [{self.mode}]"


class UserProfile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profiles"
    )

    associated_device = models.ForeignKey(
        MirrorDevice,
        on_delete=models.CASCADE,
        related_name="profiles"
    )

    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    profile_photo_url = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Profile: {self.full_name} ({self.user.username})"


class Recording(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="recordings")
    video_file_path = models.TextField()
    recorded_at = models.DateTimeField(auto_now_add=True)
    duration_seconds = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Recording for {self.profile.full_name} at {self.recorded_at}"
