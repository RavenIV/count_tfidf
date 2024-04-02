from math import log

# from django.core.validators import FileExtensionValidator
from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=150)
    # file = models.FileField(
    #     upload_to='texts',
    #     validators=[
    #         FileExtensionValidator(allowed_extensions=['.txt', '.doc', '.docx'])
    #     ]
    # )
    number_of_words = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)


class Term(models.Model):

    spelling = models.TextField(unique=True)
    documents = models.ManyToManyField(Document, through='DocumentTerms')
    inverse_frequency = models.FloatField(null=True)


    # def inverse_frequency(self):
    #     return log(Document.objects.count() / self.documents.count())


class DocumentTerms(models.Model):

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
    )
    word = models.ForeignKey(
        Term,
        on_delete=models.CASCADE,
    )
    frequency = models.FloatField()
