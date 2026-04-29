from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_users')
    password_display = models.CharField(max_length=255, null=True, blank=True)  # Store plaintext for display
    
    def __str__(self):
        return f"Profile for {self.user.username}"
