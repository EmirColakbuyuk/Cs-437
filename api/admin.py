from django.contrib import admin

from api.models import TopRanked


class TopRankedAdmin(admin.ModelAdmin):
    list_display = ('url', 'counter', 'created_at')  # Admin panelinde görüntülenecek alanlar
    search_fields = ['url']  # Arama kutusunda hangi alanlar üzerinde arama yapılabileceği

# ModelAdmin sınıfı ile modelinizi kaydedin
admin.site.register(TopRanked, TopRankedAdmin)
