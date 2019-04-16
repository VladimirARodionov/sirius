from .settings import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
LEAD_LINK = 'http://localhost:8081/sirius/crm/lead/edit/%(id)s'
APPOINTMENT_LINK = 'http://localhost:8081/sirius/zdravniza/appointment/edit/%(id)s'
