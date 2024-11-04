import uuid

from django.db import models


class UUIDPrimaryKeyField(models.Field):
    """
    A custom field that uses UUID as primary key, stored in uppercase and without hyphens.
    """

    description = "A primary key field that uses UUID in uppercase without hyphens"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 32
        kwargs['unique'] = True
        kwargs['editable'] = False
        kwargs['primary_key'] = True
        kwargs['null'] = False
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def pre_save(self, model_instance, add):
        # Generate a new UUID if the field is empty
        if add and not getattr(model_instance, self.attname):
            value = uuid.uuid4().hex.upper()  # Generate a new UUID
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)

    def deconstruct(self):
        # This is necessary for Django to be able to serialize the field
        name, path, args, kwargs = super().deconstruct()
        kwargs.update({
            'max_length': 32,
            'unique': True,
            'editable': False,
            'primary_key': True,
            'null': False
        })
        return name, path, args, kwargs
