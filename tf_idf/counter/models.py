from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now=True)


class Term(models.Model):
    spelling = models.TextField(unique=True, db_index=True)
    documents = models.ManyToManyField(Document, related_name='terms')
