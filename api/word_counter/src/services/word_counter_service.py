import re
import aiohttp
import asyncio

from api.infra.constants import InputType
from api.models import WordCount
from channels.db import database_sync_to_async
from api.infra.base_utils import logger
from api.celery import process_input_task

CHUNK_SIZE = 1024 * 1024  # 1 MB


class WordCounterService:
    @classmethod
    def get_db_semaphore(cls):
        return asyncio.Semaphore(50)

    @staticmethod
    def process_text(text):
        logger.debug(f"starting process text input")

        words = re.findall(r'\b\w+\b', text.lower())
        return words

    @staticmethod
    async def get_or_create_word_statistic_and_increment(word):
        async with WordCounterService.get_db_semaphore():
            print("hello from us")
            word_statistic, created = await database_sync_to_async(WordCount.objects.get_or_create)(word=word)
            await database_sync_to_async(word_statistic.increment)()

    @classmethod
    async def process_words(cls, words):
        print("hello from 1")

        await asyncio.gather(*(cls.get_or_create_word_statistic_and_increment(word) for word in words))

    @classmethod
    def process_file(cls, file):
        logger.debug(f"starting process input from file {file}")
        process_input_task.delay(InputType.FILE, file)

    @classmethod
    def process_url(cls, url):
        logger.debug(f"starting process input from url {url}")
        process_input_task.delay(InputType.URL, url)

    @classmethod
    def process_input(cls, input_type: InputType, input_data):
        if input_type == InputType.STRING:
            print("hello from 0")

            words = cls.process_text(input_data)

            asyncio.run(cls.process_words(words))
        elif input_type == InputType.FILE:
            cls.process_file(input_data)
        elif input_type == InputType.URL:
            cls.process_url(input_data)

    @staticmethod
    async def read_line_by_line(file_obj):
        buffer = ''
        while True:
            data = await asyncio.to_thread(file_obj.read, CHUNK_SIZE)
            if not data:
                break
            buffer += data.decode('utf-8')
            lines = buffer.splitlines(keepends=True)
            for line in lines[:-1]:
                yield line
            buffer = lines[-1]
        yield buffer

    @staticmethod
    async def read_line_by_line_response(response):
        buffer = ''
        async for chunk in response.content.iter_chunked(CHUNK_SIZE):
            buffer += chunk.decode('utf-8')
            lines = buffer.splitlines(keepends=True)
            for line in lines[:-1]:
                yield line
            buffer = lines[-1]
        yield buffer
