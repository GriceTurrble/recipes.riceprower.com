"""Managers for models in invoices app."""

from base_objects.managers import HTBaseManager

from .querysets import InvoiceQuerySet, InvoiceItemLogQuerySet


class InvoiceManager(HTBaseManager):
    queryset_class = InvoiceQuerySet


class InvoiceItemLogManager(HTBaseManager):
    queryset_class = InvoiceItemLogQuerySet

    def within_cycle(self, cycle_start, cycle_end):
        return self.get_queryset().within_cycle(cycle_start, cycle_end)

    def for_project(self, project):
        return self.get_queryset().for_project(project)
