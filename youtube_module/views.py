# Create your views here.
import os

from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from youtube_module.models import Keyword, VideoData
from youtube_module.serializers import KeywordSerializer, VideoDataSerializer
from youtube_module.utils import YoutubeClient


class YoutubeAPIViewSet(ListModelMixin, GenericViewSet):
    """
    This viewset contains endpoints pertaining to the YouTube API, searched keywords and Video Data
    """
    # * Configuration
    serializers = {
        'set_keyword': {
            "POST": KeywordSerializer,
        },
        'list': {
            "GET": VideoDataSerializer
        }
    }

    permissions = {
        'set_keyword': [IsAuthenticated],
        'list': [IsAuthenticated]
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action).get(self.request.method)

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action)

        if self.permission_classes is None:
            self.permission_classes = [IsAuthenticated]

        return super(YoutubeAPIViewSet, self).get_permissions()

    def get_queryset(self):
        if self.request.user.keyword is None:
            return None
        else:
            return VideoData.objects.filter(related_keywords__keyword=self.request.user.keyword).order_by(
                '-published_at')

    @action(methods=['post'], detail=False)
    def set_keyword(self, request, *args, **kwargs):
        """
        This endpoint sets a keyword for the current user. Any existing keyword relationships will be deleted.
        """
        user = self.request.user
        serializer = self.get_serializer_class()(data=request.data)

        serializer.is_valid(raise_exception=True)
        value = serializer.data.get('value')

        keyword = Keyword.objects.get_or_create(value=value)[0]
        user.keyword = keyword
        user.save()

        yt_client = YoutubeClient(os.environ.get('YOUTUBE_API_TOKEN'))
        yt_client.run_search(keyword=keyword.value)

        return Response({"message": "Keyword saved"}, status=HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """
        This endpoint lists all the videos related to the keyword of the current user
        """
        if request.user.keyword is None:
            return Response({"message": "No keyword set for current user"}, status=HTTP_400_BAD_REQUEST)
        else:
            return super(YoutubeAPIViewSet, self).list(self, request, *args, **kwargs)
