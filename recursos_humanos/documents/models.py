import os

from django.conf import settings
from django.db import models

from recursos_humanos.services.singleton.pinecone_singleton import PineconeSingleton
from recursos_humanos.base.models import BaseModel


class DocumentModel(BaseModel):

    class Meta:
        verbose_name = 'document'
        verbose_name_plural = 'documents'

    title = models.CharField(
        unique=True, max_length=200, help_text="Nombre o título del documento")
    description = models.TextField(
        null=False, blank=False, help_text="Descripción del documento")
    file = models.FileField(upload_to='documents/',
                            help_text="Archivo del documento")
    is_ready = models.BooleanField(
        default=False, help_text="Indica si el archivo está listo después del análisis")
    # vector_id = models.CharField(max_length=100, unique=True, help_text="ID único del documento en la base de datos vectorial")

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if self.file:
            self.vectorize_file(self.file)

        self.is_ready = True
        super().save(update_fields=['is_ready'])

    def delete(self, *args, **kwargs):

        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)

        super().delete(*args, **kwargs)

    def vectorize_file(self, file):
        PineconeSingleton.vectorize_file(file, self.title)

    def __repr__(self):
        return (f'DocumentModel(id={self.id}, '
                'title={self.title}, '
                'description={self.description}, '
                'ready={self.is_ready}, '
                'created_at={self.created_at}, '
                'updated_at={self.updated_at})')

    def __str__(self):
        return f'{self.title}'
