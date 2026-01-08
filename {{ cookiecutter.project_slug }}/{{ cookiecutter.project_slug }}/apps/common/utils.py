def has_consent(request, name: str) -> bool:
    """Returns if consent cookie is available in `request.COOKIES`.

    Args:
        request(HttpRequest) - Incoming request.
        name - Cookie name.

    Returns:
        True if cookie is in `request.COOKIES`, False otherwise.
    """
    return name in request.COOKIES


def set_consent(response, name: str) -> None:
    """Sets cookie in response.

    Args:
        response(HttpResponse) - Response object.
        name - Name of cookie.
    """
    response.set_cookie(name, 'accepted', max_age=1000)


def is_consent_accepted(request, name: str) -> bool:
    """Returns True if cookie specified by name was accepted.

    Args:
        request(HttpRequest) - Incoming request.
        name - Cookie name.

    Returns:
        True if cookie specified by name was accepted.
    """
    if has_consent(request, name):
        return request.COOKIES[name] == 'accepted'
    else:
        return False
