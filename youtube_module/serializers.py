from rest_framework import serializers

from youtube_module.models import Keyword


class KeywordSerializer(serializers.ModelSerializer):
    """
    This serializer is to be used by the user to set a keyword.
    """

    class Meta:
        model = Keyword
        fields = ['value', 'id']
        read_only_fields = ['id', ]
