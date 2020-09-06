"""Querysets for models in invoices app."""

from base_objects.querysets import ProjectBaseQuerySet


class InvoiceQuerySet(ProjectBaseQuerySet):
    pass


class InvoiceItemLogQuerySet(ProjectBaseQuerySet):
    def within_cycle(self, cycle_start, cycle_end):
        return self.filter(
            date__gte=cycle_start,
            date__lte=cycle_end,
        )

    def for_project(self, project):
        return self.filter(project=project)