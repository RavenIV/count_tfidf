from math import log
from re import findall

from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import render

from .forms import UploadTextFile
from .models import Document, Term


def count_tf(frequency: float, words_number: float) -> float:
    return frequency / words_number

def count_idf(term: Term):
    return log(Document.objects.count() / term.documents.count())


def handle_uploaded_file(file: UploadedFile):
    
    text = str(file.read(), encoding='utf-8').lower()
    words = findall(r'[^\W0-9]+', text)
    document = Document.objects.create(
        name=file.name,
        number_of_words=len(words)
    )
    words_count = {}

    for word in words:
        if word not in words_count:
            words_count[word] = 1
        else:
            words_count[word] += 1

    for word, count in words_count.items():

        term, created = Term.objects.get_or_create(spelling=word)
        term.documents.add(
            document,
            through_defaults={
                'frequency': count_tf(
                    float(count), float(document.number_of_words)
                ),
            }
        )
        Term.objects.filter(id=term.pk).update(inverse_frequency=count_idf(term))

    return document.documentterms_set.order_by('-word__inverse_frequency')[:50]



def counter_view(request):
    context = {}
    form = UploadTextFile(request.POST, request.FILES)
    if form.is_valid():
        data = handle_uploaded_file(request.FILES['file'])
        context['data'] = data
    context['form'] = form
    return render(request, 'counter.html', context)
    