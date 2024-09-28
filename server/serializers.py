from adrf.serializers import Serializer
from rest_framework import serializers


class TGUserCreateOrEditSerializer(Serializer):
    tg_id = serializers.IntegerField()
    chat_id = serializers.IntegerField()
    tg_username = serializers.CharField()
