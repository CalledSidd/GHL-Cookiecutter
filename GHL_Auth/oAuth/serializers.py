from rest_framework.serializers import Serializer
from rest_framework import serializers


class ContactSerializer(Serializer):
    id = serializers.CharField()
    locationId = serializers.CharField()
    contactName = serializers.CharField()