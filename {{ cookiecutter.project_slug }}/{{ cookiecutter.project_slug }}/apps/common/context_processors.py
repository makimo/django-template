import json

from django.conf import settings
from django.utils.html import mark_safe


def gdpr(request):
    """Attach GDPR settings to global context."""
    return {
        'GDPR_SETTINGS': mark_safe(json.dumps(settings.GDPR_SETTINGS)),
    }
