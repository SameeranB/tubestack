# Create your views here.

from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.viewsets import GenericViewSet

from youtube_module.models import Keyword, VideoData, YoutubeAPIToken
from youtube_module.serializers import KeywordSerializer, VideoDataSerializer, SetTokenSerializer
from youtube_module.utils import YoutubeClient, NoActiveTokens


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
        },
        'add_token': {
            "POST": SetTokenSerializer
        },
        'list_tokens': {
            "GET": SetTokenSerializer
        }
    }

    permissions = {
        'set_keyword': [IsAuthenticated],
        'list': [IsAuthenticated],
        'add_token': [IsAuthenticated, IsAdminUser],
        'list_tokens': [IsAuthenticated, IsAdminUser]
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

        keyword = Keyword.objects.get_or_create(value=value.lower())[0]
        user.keyword = keyword
        user.save()

        yt_client = YoutubeClient()
        try:
            yt_client.run_search(keyword=keyword.value)
        except NoActiveTokens:
            return Response({"message": "There are no active tokens available. Please contact an admin"},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message": "Keyword saved"}, status=HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """
        This endpoint lists all the videos related to the keyword of the current user
        """
        if request.user.keyword is None:
            return Response({"message": "No keyword set for current user"}, status=HTTP_400_BAD_REQUEST)
        else:
            return super(YoutubeAPIViewSet, self).list(self, request, *args, **kwargs)

    @action(methods=['post'], detail=False)
    def add_token(self, request, *args, **kwargs):
        """
        This endpoint is to be used by admins to add a new API Token
        """
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(active=True, units=0)
        return Response({'message': "Token added"}, status=HTTP_201_CREATED)

    @action(methods=['get'], detail=False)
    def list_tokens(self, request, *args, **kwargs):
        """
        This endpoint is to be used by admins to list all API tokens
        """
        serializer = self.get_serializer_class()(data=YoutubeAPIToken.objects.all(), many=True)
        serializer.is_valid()
        return Response(serializer.data, status=HTTP_200_OK)
