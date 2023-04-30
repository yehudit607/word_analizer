import asyncio

from asgiref.sync import async_to_sync
from rest_framework.views import APIView
from django.http import JsonResponse
from api.word_counter.schema import WordCounterInputSchema
from api.word_counter.src.services.word_counter_service import WordCounterService


class WordCounterView(APIView):

    def post(self, request):
        serializer = WordCounterInputSchema(data=request.data)
        serializer.is_valid(raise_exception=True)

        input_type = None
        input_data = None
        if serializer.validated_data.get('text'):
            input_type = 'string'
            input_data = serializer.validated_data['text']
        elif serializer.validated_data.get('file'):
            input_type = 'file'
            input_data = serializer.validated_data['file']
        elif serializer.validated_data.get('url'):
            input_type = 'url'
            input_data = serializer.validated_data['url']
        else:
            return JsonResponse({"detail": "No input provided."}, status=400)

        process_input_sync = async_to_sync(WordCounterService.process_input)
        process_input_sync(input_type, input_data)

        return JsonResponse({"detail": "Word counting completed."}, status=200)
