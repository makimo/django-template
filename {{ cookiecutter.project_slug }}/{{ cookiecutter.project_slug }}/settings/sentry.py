import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import env

sentry_sdk.init(
    dsn=env('SENTRY_DSN', default=''),
    integrations=[DjangoIntegration()],
    send_default_pii=True # If True associate users to errors
)
