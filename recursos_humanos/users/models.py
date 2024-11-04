from enum import Enum

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from ..base.models import BaseModel
from .custom_fields import UUIDPrimaryKeyField


__author__ = 'Ricardo'
__version__ = '0.1'


# -------------------------------------------------------------
#                             User
# -------------------------------------------------------------


class UserManager(BaseUserManager):

    def create_user(self, first_name, middle_name, last_name, username, password, is_staff, is_active, is_superuser=False):
        user = self.model(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            username=username,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, middle_name, last_name, username, password):
        return self.create_user(first_name, middle_name, last_name, username, password, True, True, True)


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    This model define an user
    """

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        indexes = [
            models.Index(name='user_id_idx', fields=['id']),
        ]

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'middle_name', 'last_name']

    objects = UserManager()
    first_name = models.CharField(unique=True, max_length=50,
                                  null=False, blank=False)
    middle_name = models.CharField(
        unique=True, max_length=50, null=False, blank=False,)
    last_name = models.CharField(
        unique=True, max_length=50, null=False, blank=False,)
    username = models.CharField(
        unique=True, max_length=20, null=False, blank=False,)
    contract_type = models.CharField(
        max_length=20, null=True, blank=True,)
    base_salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,)
    vacation_days = models.IntegerField(null=True, blank=True,)
    job_title = models.CharField(max_length=50, null=False, blank=False,)
    department = models.CharField(max_length=50, null=False, blank=False,)
    plant = models.CharField(max_length=50, null=False, blank=False,)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    def __repr__(self):
        return (f'UserModel('
                f'id={self.id}, '
                f'first_name={self.first_name}, '
                f'middle_name={self.middle_name}, '
                f'last_name={self.last_name}, '
                f'username={self.username}, '
                f'contract_type={self.contract_type}, '
                f'base_salary={self.base_salary}, '
                f'vacation_days={self.vacation_days}, '
                f'job_title={self.job_title}, '
                f'department={self.department}, '
                f'plant={self.plant}, '
                f'is_staff={self.is_staff}, '
                f'is_active={self.is_active})')


# -------------------------------------------------------------
#                     Conversation thread
# -------------------------------------------------------------


class RoleEnum(Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'

    @classmethod
    def choices(cls):
        return [(choice.value, choice.name) for choice in cls]


class ConversationThreadModel(BaseModel):

    class Meta:
        verbose_name = 'conversation thread'
        verbose_name_plural = 'conversation threads'
        indexes = [
            models.Index(name='conversation_thread_id_idx', fields=['id']),
        ]

    id = UUIDPrimaryKeyField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'

    def __repr__(self):
        return (f'ConversationThreadModel('
                f'id={self.id}, '
                f'user={self.user})')


class ConversationMessageModel(BaseModel):

    class Meta:
        verbose_name = 'conversation message'
        verbose_name_plural = 'conversation messages'
        indexes = [
            models.Index(name='conversation_message_id_idx', fields=['id']),
        ]

    conversation_thread = models.ForeignKey(
        ConversationThreadModel, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20, choices=RoleEnum.choices(), blank=False, null=False)
    message = models.TextField(null=False, blank=False)

    def __str__(self):
        return f'{self.id}'

    def __repr__(self):
        return (f'ConversationMessageModel(id={self.id}, '
                f'conversation_thread={self.conversation_thread}, '
                f'message={self.message})')
