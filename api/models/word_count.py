from django.db import models
from channels.db import database_sync_to_async


class WordCount(models.Model):
    word = models.CharField(max_length=255, db_index=True)
    count = models.IntegerField(default=0)

    @database_sync_to_async
    def increment(self):
        self.count += 1
        self.save()

    class Meta:
        unique_together = ('word',)
