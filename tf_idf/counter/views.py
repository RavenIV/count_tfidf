from django.shortcuts import render

from .models import Document
from .utils import (
    retrieve_words,
    count_number_of_each_word,
    set_document_terms,
    count_tf_idf
)

WORDS_NOT_FOUND = 'Упс! В файле нет слов. Попробуйте загрузить другой файл.'


def counter_view(request):
    context = {}
    if request.method == 'POST' and request.FILES['text_file']:
        file = request.FILES['text_file']
        words = retrieve_words(file)
        if words:
            document = Document.objects.create(name=file.name)
            words_count = count_number_of_each_word(words)
            set_document_terms(document, list(words_count.keys()))
            context['data'] = count_tf_idf(document, len(words), words_count)
        else:
            context['error'] = WORDS_NOT_FOUND
    return render(request, 'counter.html', context)
