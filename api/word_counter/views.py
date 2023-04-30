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
            'file': request.FILES.get('file'),
            'url': serializer.validated_data.get('url'),
        }

        input_type, input_value = next(((key, value) for key, value in input_data.items() if value), (None, None))

        if not input_value:
            return JsonResponse({"detail": "No input provided."}, status=HTTPStatus.BAD_REQUEST)

        if input_type == 'file':
            input_value = self._handle_file_input(input_value)

        try:
            word_counter_service = WordCounterService()
            await word_counter_service.process_input_async(input_type, input_value)
            return JsonResponse({"detail": "Word counting completed."}, status=HTTPStatus.OK)
        except Exception as e:
            return JsonResponse({"detail": f"An error occurred: {str(e)}"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    @staticmethod
    def _handle_file_input(input_value):
        if hasattr(input_value, 'temporary_file_path'):
            return input_value.temporary_file_path()
        else:
            # If the file is small and stored in memory, read the content
            return io.StringIO(input_value.read().decode('utf-8'))


