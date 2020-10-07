from django.contrib import admin

# Register your models here.
from youtube_module.models import Keyword, VideoData, VideoKeywordRelationship

admin.site.register(Keyword)
admin.site.register(VideoData)
admin.site.register(VideoKeywordRelationship)