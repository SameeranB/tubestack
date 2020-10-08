from django.db import IntegrityError
from googleapiclient.discovery import build
from rest_framework.exceptions import APIException

from youtube_module.models import VideoData, VideoKeywordRelationship, Keyword, YoutubeAPIToken


class YoutubeClient:
    """
    This is a client wrapper for the client provided by Google.
    It helps maintain DRY and also allows the search to be run as a function by a scheduler
    """

    def __init__(self):
        """
        The youtube data api service is built using the token provided on instantiation.
        """
        self.token = get_active_token()
        try:
            self.service = build('youtube', 'v3', developerKey=self.token.token)
        except Exception as e:
            self.token.active = False
            self.token.save()
            raise NoActiveTokens

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

        try:
            response = request.execute()
        except Exception as e:
            self.token.active = False
            self.token.save()
            raise NoActiveTokens

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


class NoActiveTokens(APIException):
    status_code = 500
    default_detail = 'There are no active tokens. Please add one to continue'
    default_code = 'service_unavailable'


def get_active_token():
    token_instance = YoutubeAPIToken.objects.filter(active=True).first()
    if not token_instance:
        raise NoActiveTokens
    token_instance.units += 100
    token_instance.save()
    if token_instance.units >= 10000:
        token_instance.active = False
        token_instance.save()

    return YoutubeAPIToken.objects.filter(active=True).first()
