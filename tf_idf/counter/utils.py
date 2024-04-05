from math import log
from re import findall
from typing import Optional

from django.core.files.uploadedfile import UploadedFile
from django.db.models import Count

from .models import Document, Term


def retrieve_words(file: UploadedFile) -> Optional[list[str]]:
    """Читает содержимое файла и находит все слова."""
    return findall(
        r'[^\W0-9]+',
        str(file.read(), encoding='utf-8').lower()
    )


def count_number_of_each_word(words: list[str]) -> dict[str, int]:
    """Считает, сколько раз каждое слово встречается в документе."""
    words_count = {}
    for word in words:
        if word not in words_count:
            words_count[word] = 0
        words_count[word] += 1
    return words_count


def set_document_terms(document: Document, text_words: list[str]):
    """Обрабатывает список слов (без повторов) и обновляет записи в БД."""
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
    """
    Формирует данные в виде списка кортежей,
    в каждом из которых три элемента: (<слово>, <TF>, <IDF>).
    Для подсчета IDF в качестве корпуса используются
    все ранее обработанные файлы.
    """
    terms = Term.objects.annotate(
        doc_count=Count('documents')
    ).filter(documents__id=document.pk)
    total_documents = Document.objects.count()
    data = [
        (
            term.spelling,
            round(words_count[term.spelling] / total_words, 4),
            round(log(total_documents / term.doc_count), 4)
        ) for term in terms
    ]
    data.sort(key=lambda tup: (-tup[2], -tup[1], tup[0]))
    return data
