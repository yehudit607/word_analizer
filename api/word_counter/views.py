import io
from asgiref.sync import async_to_sync
from rest_framework.views import APIView
from django.http import JsonResponse
from api.word_counter.schema import WordCounterInputSchema
from api.word_counter.src.services.word_counter_service import WordCounterService
from http import HTTPStatus


class WordCounterView(APIView):
    @async_to_sync
    async def post(self, request):
        serializer = WordCounterInputSchema(data=request.data)
        serializer.is_valid(raise_exception=True)

        input_data = {
            'string': serializer.validated_data.get('text'),
            'file_path': serializer.validated_data.get('file_path'),
            'url': serializer.validated_data.get('url'),
        }

        input_type, input_value = next(((key, value) for key, value in input_data.items() if value), (None, None))

        if not input_value:
            return JsonResponse({"detail": "No input provided."}, status=HTTPStatus.BAD_REQUEST)

        try:
            word_counter_service = WordCounterService()
            await word_counter_service.process_input_async(input_type, input_value)
            return JsonResponse({"detail": "Word counting completed."}, status=HTTPStatus.OK)
        except Exception as e:
            return JsonResponse({"detail": f"An error occurred: {str(e)}"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

