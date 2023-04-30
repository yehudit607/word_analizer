from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.word_statistics.schema import WordStatisticsInputSchema
from api.word_statistics.service import WordStatisticsService


class WordStatisticsView(APIView):

    def get(self, request):
        serializer = WordStatisticsInputSchema(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        word = serializer.validated_data['word']
        count = WordStatisticsService.get_word_count(word)

        return Response({"count": count}, status=status.HTTP_200_OK)
