# Remove module when django-fractions updates for Django 4.0 compatibility


def patch_lazy_translation():
    """Makes ugettext_lazy and ungettext_lazy available as wrappers
    for gettext_lazy and ngettext_lazy, respectively.

    django-fractions 2.0.0 still calls in ugettext_lazy and ungettext_lazy.
    Until a patch for django-fractions corrects this,
    this fix makes the "old" ones act like the new.
    """
    import django
    from django.utils.translation import gettext_lazy, ngettext_lazy

    django.utils.translation.ugettext_lazy = gettext_lazy
    django.utils.translation.ungettext_lazy = ngettext_lazy
