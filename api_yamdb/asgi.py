"""
ASGI config for YaMDb project.
<<<<<<< HEAD

It exposes the ASGI callable as a module-level variable named ``application``.

=======
It exposes the ASGI callable as a module-level variable named ``application``.
>>>>>>> titles
For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')

application = get_asgi_application()
