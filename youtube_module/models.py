from django.db import models


# Create your models here.


class Keyword(models.Model):
    value = models.CharField(max_length=300)


class VideoData(models.Model):
    video_id = models.CharField(max_length=12, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.URLField()
    channel_name = models.CharField(max_length=300)
    published_at = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=['video_id', 'published_at'])]
        ordering = ['video_id', '-published_at']
        verbose_name_plural = "VideosData"


class VideoKeywordRelationship(models.Model):
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='related_videos')
    video = models.ForeignKey(VideoData, on_delete=models.CASCADE, related_name='related_keywords')

