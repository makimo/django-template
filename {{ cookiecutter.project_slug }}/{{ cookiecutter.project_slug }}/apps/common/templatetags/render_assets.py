from django import template
from django.utils.safestring import mark_safe

from ..utils import get_static_url

register = template.Library()


@register.simple_tag
def render_js(resource_path):
    """Gets full url for javascript file with HTML tag.

    Args:
        resource_path - Path to javascript file in webserver without extension
    Returns:
        HTML tag with full url to javascript file.
    """
    url = get_static_url(resource_path, extension='js')

    if url:
        return mark_safe('<script type="text/javascript" src="{}"></script>'.format(url))
    else:
        return ''


@register.simple_tag
def render_css(resource_path):
    """Gets full url for css file with HTML tag.

    Args:
        resource_path - Path to css file in webserver without extension
    Returns:
        HTML tag with full url to css file.
    """
    url = get_static_url(resource_path, extension='css')

    if url:
        return mark_safe('<link rel="stylesheet" href="{}">'.format(url))
    else:
        return ''


@register.simple_tag
def static_image(resource_path):
    """Gets full path to image file wih HTML tag.

    Args:
        resource_path - Path to image in webserver without extension.
    Returns:
        HTML tag with full url to image file.
    """
    return get_static_url(resource_path)

