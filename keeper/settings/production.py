from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['.herokuapp.com', 'localhost', '127.0.0.1', '[::1]']

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Django-storages for using AWS S3 bucket
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'keeperapp/static'),
# )

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'keeperapp-assets'
AWS_DEFAULT_ACL = None
AWS_REGION = 'us-east-2'
# AWS_S3_SIGNATURE_VERSION = True
S3_USE_SIGV4 = 1

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION = 'static'
AWS_STATIC_LOCATION = 'static'
AWS_MEDIA_LOCATION = 'media'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://s3.%s.amazonaws.com/%s/%s/" % (AWS_REGION, AWS_STORAGE_BUCKET_NAME, AWS_STATIC_LOCATION)
# MEDIA_ROOT = "https://s3.us-east-2.amazonaws.com/keeperapp-assets"
MEDIA_URL = "https://s3.%s.amazonaws.com/%s/%s/" % (AWS_REGION, AWS_STORAGE_BUCKET_NAME, AWS_MEDIA_LOCATION)

DEFAULT_FILE_STORAGE = 'keeperapp.storage_backends.MediaStorage'

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
