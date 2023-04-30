from django.urls import path

from api.word_counter.views import WordCounterView
from api.word_statistics.views import WordStatisticsView

#from .word_statistics.views import WordStatisticsView

urlpatterns = [
    path('wordcounter/', WordCounterView.as_view(), name='word_counter'),
    path('wordstatistics/', WordStatisticsView.as_view(), name='word_statistics'),


]
