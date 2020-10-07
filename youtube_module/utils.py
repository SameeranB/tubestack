from googleapiclient.discovery import build


class YoutubeClient:
    def __init__(self, api_token):
        self.service = build('youtube', 'v3', developerKey=api_token)

    def run_search(self, keyword):
        request = self.service.search().list(
            part="snippet",
            maxResults=25,
            q=keyword
        )

        response = request.execute()
        return response

    def __del__(self):
        self.service.close()
