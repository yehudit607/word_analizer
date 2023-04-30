from rest_framework import serializers


class WordCounterInputSchema(serializers.Serializer):
    text = serializers.CharField(required=False)
    file = serializers.FileField(required=False)
    url = serializers.URLField(required=False)
