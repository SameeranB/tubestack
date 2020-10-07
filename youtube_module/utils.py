from googleapiclient.discovery import build

from youtube_module.models import VideoData, VideoKeywordRelationship


class YoutubeClient:
    def __init__(self, api_token):
        self.service = build('youtube', 'v3', developerKey=api_token)

    def run_search(self, keyword):
        request = self.service.search().list(
            part="snippet",
            maxResults=25,
            q=keyword.value
        )

        response = request.execute()
        for item in response['items']:
            video = VideoData.objects.get_or_create(
                video_id=item['id']['videoId'],
                title=item['snippet']['title'],
                description=item['snippet']['description'],
                thumbnail=item['snippet']['thumbnails']['default']['url'],
                channel_name=item['snippet']['channelTitle'],
                published_at=item['snippet']['publishedAt'],
            )

            keyword_relationship = VideoKeywordRelationship.objects.create(keyword=keyword, video=video[0])
            keyword_relationship.save()

        return

    def __del__(self):
        self.service.close()
