import json

from django.db import models
# Create your models here.
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Keyword(models.Model):
    value = models.CharField(max_length=300)

    def save(self, *args, **kwargs):
        super(Keyword, self).save(*args, **kwargs)
        schedule = IntervalSchedule.objects.create(
            every=10,
            period=IntervalSchedule.SECONDS
        )
        PeriodicTask.objects.create(
            interval=schedule,
            name=f'Keyword Scheduler {self.value}',
            task='youtube_module.tasks.run_keyword_search',
            args=json.dumps([self.value])
        )


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
