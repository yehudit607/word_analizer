from api.models import WordCount


class WordStatisticsService:

    @staticmethod
    def get_word_count(word):
        word_obj = WordCount.objects.filter(word=word).first()
        if word_obj:
            return word_obj.count
        return 0
