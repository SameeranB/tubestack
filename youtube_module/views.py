# Create your views here.
import os

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from tubestack_backend.utils import YoutubeClient
from youtube_module.models import Keyword
from youtube_module.serializers import KeywordSerializer


class YoutubeAPIViewSet(GenericViewSet):

    # * Configuration
    serializers = {
        'set_keyword': {
            "POST": KeywordSerializer,
        },
    }

    permissions = {
        'set_keyword': [IsAuthenticated]
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action).get(self.request.method)

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action)

        if self.permission_classes is None:
            self.permission_classes = [IsAuthenticated]

        return super(YoutubeAPIViewSet, self).get_permissions()

    @action(methods=['post'], detail=False)
    def set_keyword(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer_class()(data=request.data)

        serializer.is_valid(raise_exception=True)
        value = serializer.data.get('value')

        keyword = Keyword.objects.get_or_create(value=value)
        user.keyword = keyword
        user.save()

        api_instance = YoutubeClient(os.environ.get('YOUTUBE_API_TOKEN'))
        response = api_instance.run_search(keyword=keyword.value)

        return Response(response, status=HTTP_200_OK)
