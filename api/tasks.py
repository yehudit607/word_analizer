import asyncio

from celery import shared_task


@shared_task(bind=True)
def process_input_task(self, input_type, input_data):
    from api.word_counter.src.services.word_counter_service import WordCounterService
    WordCounterService.process_input(input_type, input_data)


