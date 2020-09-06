from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from invoices.models import Project


class Command(BaseCommand):
    help = (
        "Generates a new invoice for the previous billing cycle for a given Project ID"
    )

    def add_arguments(self, parser):
        parser.add_argument("project_ids", nargs="+", type=int)
        parser.add_argument(
            "-d",
            "--date",
            type=str,
            default="today",
            help=(
                "Invoice date in ISO format (YYYY-MM-DD). "
                "You may also use `today` to specify today's date "
                "(this is the default)"
            ),
        )

    def handle(self, *args, **options):
        inv_date = options["date"]
        if inv_date.lower() == "today":
            invoice_date = timezone.localtime().date()
        else:
            try:
                invoice_date = timezone.datetime(*map(int, inv_date.split("-"))).date()
            except Exception as exc:
                raise CommandError(
                    "Cannot process date string: must be in YYYY-MM-DD format"
                ) from exc

        for project_id in options["project_ids"]:
            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                raise CommandError('Project "%s" not found' % project_id)

            invoice = project.generate_invoice(invoice_date)
            self.stdout.write(
                self.style.SUCCESS(f'Invoice ID {invoice.id} created: "{invoice}"')
            )
