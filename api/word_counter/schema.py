from rest_framework import serializers


class WordCounterInputSchema(serializers.Serializer):
    text = serializers.CharField(required=False)
    file_path = serializers.CharField(required=False)
    url = serializers.URLField(required=False)
