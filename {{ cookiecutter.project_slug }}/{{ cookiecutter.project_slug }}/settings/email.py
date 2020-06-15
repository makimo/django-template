import os

EMAIL_BACKEND = os.getenv(
    'EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend'
)

EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'False') == 'True'
EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_PORT = os.getenv('EMAIL_PORT', 25)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

INFO_MAIL_ACCOUNT = os.getenv('INFO_MAIL_ACCOUNT', 'no-reply@example.com')

DEFAULT_FROM_EMAIL = INFO_MAIL_ACCOUNT
SERVER_EMAIL = INFO_MAIL_ACCOUNT
