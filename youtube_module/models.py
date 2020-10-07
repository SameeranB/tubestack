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
    keyword = models.ForeignKey(Keyword, models.CASCADE, related_name='keyword')

    class Meta:
        indexes = [models.Index(fields=['keyword', 'published_at'])]
        ordering = ['keyword', '-published_at']
        verbose_name_plural = "VideosData"
