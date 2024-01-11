from django.contrib import admin
from .models import Comment, News

class CommentAdmin(admin.ModelAdmin):
    list_display = ('news_link', 'user', 'content', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('content', 'user__username')

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_time')
    list_filter = ('category', 'published_time')


admin.site.register(Comment, CommentAdmin)
admin.site.register(News, NewsAdmin)
