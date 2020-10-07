from rest_framework import routers

from youtube_module.views import YoutubeAPIViewSet

YoutubeRouter = routers.DefaultRouter(trailing_slash=False)

YoutubeRouter.register('youtube', YoutubeAPIViewSet, basename='youtube')
