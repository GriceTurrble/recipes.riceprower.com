"""Base Admin settings for the site."""

from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models

from tinymce.widgets import TinyMCE


class PageAdmin(FlatPageAdmin):
    """Admin overrides for flatpages."""

    formfield_overrides = {
        models.TextField: {"widget": TinyMCE(attrs={"cols": 100, "rows": 15})},
    }


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, PageAdmin)
