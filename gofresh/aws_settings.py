from gofresh.settings import *

ALLOWED_HOSTS = ['127.0.0.1', '54.67.89.9']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gofresh',
        'USER': 'ergoventures',
        'PASSWORD': 'ergo2016',
        'HOST': 'gofresh.ctgpx7i8fqnt.us-west-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}

INSTALLED_APPS += ('storages',)

AWS_ACCESS_KEY_ID = 'AKIAIZUG5ATPN3D3SF7Q'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'gofreshergo'
AWS_S3_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME


DEFAULT_FILE_STORAGE = 'gofresh.aws_storage_classes.MediaStorage'
STATICFILES_STORAGE = 'gofresh.aws_storage_classes.StaticStorage'

STATIC_URL = 'https://%s/static/' % AWS_S3_DOMAIN
MEDIA_URL = 'https://%s/media/' % AWS_S3_DOMAIN

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # Include the default Django email handler for errors
        # This is what you'd get without configuring logging at all.
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
             # But the emails are plain text by default - HTML is nicer
            'include_html': True,
        },
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/django/gofresh.log'
        },
    },
    'loggers': {
        # Again, default Django configuration to email unhandled exceptions
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # Might as well log any errors anywhere else in Django
        'django': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Your own app - this assumes all your logger names start with "myapp."
        'myapp': {
            'handlers': ['logfile'],
            'level': 'WARNING', # Or maybe INFO or DEBUG
            'propagate': False
        },
    },
}

