from django.contrib import admin

from api.models import TopRanked


class TopRankedAdmin(admin.ModelAdmin):
    list_display = ('url', 'counter', 'created_at')
    search_fields = ['url']


admin.site.register(TopRanked, TopRankedAdmin)
