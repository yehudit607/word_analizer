from rest_framework import serializers


class WordStatisticsInputSchema(serializers.Serializer):
    word = serializers.CharField()
