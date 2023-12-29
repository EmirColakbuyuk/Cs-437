from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    news_link = models.URLField()  # Haber linki
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Yorum yapan kullanıcı
    content = models.TextField()  # Yorum içeriği
    created_at = models.DateTimeField(auto_now_add=True)  # Yorumun oluşturulma zamanı

    def __str__(self):
        return f"Comment by {self.user.username} on {self.news_link}"