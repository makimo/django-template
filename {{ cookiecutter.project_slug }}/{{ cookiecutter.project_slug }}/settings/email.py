import os

from .base import env

EMAIL_BACKEND = env(
    'EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend'
)

EMAIL_CONFIG = env.email_url(
    'EMAIL_URL', default='smtp://user:password@localhost:25')

vars().update(EMAIL_CONFIG)

INFO_MAIL_ACCOUNT = env('INFO_MAIL_ACCOUNT', default='no-reply@example.com')

DEFAULT_FROM_EMAIL = INFO_MAIL_ACCOUNT
SERVER_EMAIL = INFO_MAIL_ACCOUNT
