from django import template
from django.utils.safestring import mark_safe

from ..utils import is_consent_accepted

register = template.Library()


@register.simple_tag
def gdpr_settings():
    """Render GDPR_SETTINGS to template inside script tag."""
    return mark_safe(
        '<script type="text/javascript">GDPR_SETTINGS = {{ "{{ GDPR_SETTINGS }}" }}</script>')


@register.simple_tag(takes_context=True)
def is_consent_accepted(context, name):
    request = context['request']

    return is_consent_accepted(request, name)
