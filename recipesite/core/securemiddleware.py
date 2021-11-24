"""Implementation of Secure.

Mostly copied from their docs:
https://secure.readthedocs.io/en/latest/frameworks.html#django
"""

import secure

secure_headers = secure.Secure()


def set_secure_headers(get_response):
    """Add secure headers to responses."""

    def middleware(request):
        response = get_response(request)
        secure_headers.framework.django(response)
        return response

    return middleware
