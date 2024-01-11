from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    news_link = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.news_link}"

#


class News(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True, unique=True)
    image_url = models.TextField(null=True, blank=True)
    published_time = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)