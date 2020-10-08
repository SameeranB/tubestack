from django.db import IntegrityError
from googleapiclient.discovery import build

from youtube_module.models import VideoData, VideoKeywordRelationship, Keyword


class YoutubeClient:
    """
    This is a client wrapper for the client provided by Google.
    It helps maintain DRY and also allows the search to be run as a function by a scheduler
    """

    def __init__(self, api_token):
        """
        The youtube data api service is built using the token provided on instantiation.
        """
        self.service = build('youtube', 'v3', developerKey=api_token)

    def run_search(self, keyword):
        """
        The search for the provided keyword is ran here.
        """
        request = self.service.search().list(
            part="snippet",
            type="video",
            maxResults=25,
            q=keyword
        )

        response = request.execute()

        # This loop iterates over the response, checks if the video exists then adds it. It also adds a relationship
        # between the video and the keyword
        for item in response['items']:
            try:
                video = VideoData.objects.get_or_create(
                    video_id=item['id']['videoId'],
                    title=item['snippet']['title'],
                    description=item['snippet']['description'],
                    thumbnail=item['snippet']['thumbnails']['default']['url'],
                    channel_name=item['snippet']['channelTitle'],
                    published_at=item['snippet']['publishedAt'],
                )
                keyword_instance = Keyword.objects.get(value=keyword)

                keyword_relationship = VideoKeywordRelationship.objects.create(keyword=keyword_instance, video=video[0])
                keyword_relationship.save()
            except IntegrityError:
                pass
        return
