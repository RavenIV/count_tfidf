

from math import log
from re import findall
from typing import Optional

from django.core.files.uploadedfile import UploadedFile
from django.db.models import Count

from .models import Document, Term


def retrieve_words(file: UploadedFile) -> Optional[list[str]]:
    words = []
    line = file.readline()
    while line:
        words += findall(
            r'[^\W0-9]+',
            str(file.readline(), encoding='utf-8').lower()
        )
    return words


def count_number_of_each_word(words: list[str]) -> dict[str, int]:
    words_count = {}
    for word in words:
        if word not in words_count:
            words_count[word] = 0
        words_count[word] += 1
    return words_count


def set_document_terms(document: Document, text_words: list[str]):
    new_words = []
    existing_terms = []
    db_terms = Term.objects.in_bulk(field_name='spelling')
    for word in text_words:
        if word in db_terms:
            existing_terms.append(db_terms[word])
        else:
            new_words.append(word)

    new_terms = Term.objects.bulk_create(
        Term(spelling=word) for word in new_words
    )
    existing_terms += new_terms
    document.terms.set(existing_terms)


def count_tf_idf(
        document: Document,
        total_words: int,
        words_count: dict[str, int]
) -> list[tuple[str, float, float]]:
    terms = Term.objects.annotate(doc_count=Count('documents')).filter(
        documents__id=document.pk
    )
    total_documents = Document.objects.count()
    data = [
        (
            term.spelling,
            words_count[term.spelling] / total_words,
            log(total_documents / term.doc_count)
        ) for term in terms
    ]
    data.sort(key=lambda x: x[2], reverse=True)
    return data[:50]