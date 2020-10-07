# Create your views here.

from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from youtube_module.models import Keyword, VideoData
from youtube_module.serializers import KeywordSerializer, VideoDataSerializer


class YoutubeAPIViewSet(ListModelMixin, GenericViewSet):
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
        return VideoData.objects.filter(related_keywords__keyword=self.request.user.keyword).order_by('-published_at')

    @action(methods=['post'], detail=False)
    def set_keyword(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer_class()(data=request.data)

        serializer.is_valid(raise_exception=True)
        value = serializer.data.get('value')

        keyword = Keyword.objects.get_or_create(value=value)[0]
        user.keyword = keyword
        user.save()

        return Response({"message": "Keyword saved"}, status=HTTP_200_OK)
