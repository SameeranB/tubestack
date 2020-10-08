from django.contrib import admin
# Register your models here.
from django.contrib.admin.options import ModelAdmin

from youtube_module.models import Keyword, VideoData, VideoKeywordRelationship


@admin.register(Keyword)
class KeywordAdmin(ModelAdmin):
    list_display = ('value',)
    ordering = ('value',)


@admin.register(VideoData)
class VideoDataAdmin(ModelAdmin):
    list_display = ('video_id', 'title', 'channel_name', 'published_at')
    list_filter = ('published_at', 'channel_name', 'related_keywords')
    ordering = ('video_id',)
    search_fields = ('title', 'description')


@admin.register(VideoKeywordRelationship)
class VideoKeywordRelationshipAdmin(ModelAdmin):
    list_display = ('keyword', 'video')
    list_filter = ('keyword__value',)
    ordering = ('keyword', 'video')
