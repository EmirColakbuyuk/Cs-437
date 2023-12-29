from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('news_link', 'user', 'content', 'created_at')  # Admin panelinde gösterilecek alanlar
    list_filter = ('created_at', 'user')  # Filtreleme seçenekleri
    search_fields = ('content', 'user__username')  # Arama çubuğunda arama yapılacak alanlar

admin.site.register(Comment, CommentAdmin)
