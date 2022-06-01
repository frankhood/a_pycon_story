from rest_framework import serializers

from pycon_service.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ("id", "name", "file", "created", "modified")
