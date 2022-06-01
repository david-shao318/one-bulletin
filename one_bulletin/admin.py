from django.contrib import admin
from .models import NewsStory


@admin.register(NewsStory)
class NewsStoryAdmin(admin.ModelAdmin):
    list_display = ("sources", "headline", "date_time")
