import re
import aiohttp
import asyncio

from api.infra.constants import InputType
from api.models import WordCount
from channels.db import database_sync_to_async
from api.infra.base_utils import logger
import aiofiles

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
            word_statistic, created = await database_sync_to_async(WordCount.objects.get_or_create)(word=word)
            await database_sync_to_async(word_statistic.increment)()

    @classmethod
    async def process_words(cls, words):
        await asyncio.gather(*(cls.get_or_create_word_statistic_and_increment(word) for word in words))

    async def process_input_async(self, input_type: InputType, input_data):
        try:
            if input_type == InputType.STRING:
                words = self.process_text(input_data)
                await self.process_words(words)
            elif input_type == InputType.FILE:
                async with aiofiles.open(input_data, mode='r') as file:
                    async for line in self.read_line_by_line(file):
                        words = self.process_text(line)
                        await self.process_words(words)
            elif input_type == InputType.URL:
                async with aiohttp.ClientSession() as session:
                    async with session.get(input_data) as response:
                        if response.status != 200:
                            raise Exception(f"Failed to fetch URL content. Status code: {response.status}")
                        async for line in self.read_line_by_line_response(response):
                            words = self.process_text(line)
                            await self.process_words(words)
            return str(input_type)
        except Exception as e:
            logger.error(f"Error processing input of type {input_type}: {e}")
            raise

    @staticmethod
    async def read_line_by_line(file_obj):
        buffer = ''
        while True:
            data = await file_obj.readline()
            if not data:
                break
            buffer += data
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
