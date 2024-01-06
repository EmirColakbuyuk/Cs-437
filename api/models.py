from django.db import models

class TopRanked(models.Model):
    url = models.CharField(max_length=200)  # Uzunluğu artır
    counter = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

