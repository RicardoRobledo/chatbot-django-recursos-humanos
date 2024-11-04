from .base import BASE_DIR

from decouple import config
import os


DEBUG = True

ALLOWED_HOSTS = ['*']

os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

DATABASES = {
    'default': {
        'ENGINE': config('ENGINE'),
        'NAME': config('NAME'),
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
        'HOST': config('HOST'),
        'PORT': config('PORT'),
    }
}
