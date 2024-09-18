import uuid
from django.db import models
from django.contrib.auth.models import User # Menghubungkan Model MoodEntry dengan User

# Create your models here.
class MoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # menghubungkan satu mood entry dengan satu user melalui sebuah relationship
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mood = models.CharField(max_length=255)
    time = models.DateField(auto_now_add=True)
    feelings = models.TextField()
    mood_intensity = models.IntegerField()

    @property
    def is_mood_strong(self):
        return self.mood_intensity > 5