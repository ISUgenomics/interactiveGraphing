from django.db import models
from django.contrib.sessions.models import Session

class AppState(models.Model):
    session_key = models.CharField(max_length=40, default='default_session_key')
    app_name = models.CharField(max_length=100)
    app_instance = models.IntegerField()
    state_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.app_name}-{self.app_instance}"
