from rest_framework import serializers

from youtube_module.models import Keyword, VideoData, YoutubeAPIToken


class KeywordSerializer(serializers.ModelSerializer):
    """
    This serializer is to be used by the user to set a keyword.
    """

    class Meta:
        model = Keyword
        fields = ['value', 'id']
        read_only_fields = ['id', ]


class VideoDataSerializer(serializers.ModelSerializer):
    """
    This serializer is to be used by the user to retrieve a list of videos related to his/her keyword
    """

    class Meta:
        model = VideoData
        fields = '__all__'


class SetTokenSerializer(serializers.ModelSerializer):
    """
    This serializer is to be used by admins to add new API tokens
    """

    class Meta:
        model = YoutubeAPIToken
        fields = '__all__'
        read_only_fields = ['id', 'active', 'units']
