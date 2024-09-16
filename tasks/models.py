from django.db import models
from django.contrib.auth.models import User

class Manage(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)  # False for pending, True for completed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
