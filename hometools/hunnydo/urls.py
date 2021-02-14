"""Urls for `hunnydo` app."""

from django.urls import path, include

from . import views


# Default app name to use for namespacing this app's URLs.
# (a template url must include `hunnydo:` as a prefix to reach here).
# https://docs.djangoproject.com/en/3.0/topics/http/urls/#url-namespaces-and-included-urlconfs
app_name = "hunnydo"

urlpatterns = [
    # Standard view paths and other includes can go here!
]
