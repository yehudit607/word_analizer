from django.urls import path
from . import views

urlpatterns = [
    path('wordcounter/', views.WordCounterView.as_view(), name='word_counter'),
]
