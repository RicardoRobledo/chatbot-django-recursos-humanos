"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')


def initialize_connections():
    """
    Funcion para inicializar datos en la aplicacion.
    Esto podria ser cargar datos de configuracion, verificar conexiones, etc.
    """

    from recursos_humanos.services.singleton.openai_singleton import OpenAISingleton
    from recursos_humanos.services.singleton.pinecone_singleton import PineconeSingleton

    print('Initializing connections...')
    print('OpenAI...')
    OpenAISingleton()
    print('Pinecone...')
    PineconeSingleton()
    print('Connections initialized.')


initialize_connections()
application = get_wsgi_application()
