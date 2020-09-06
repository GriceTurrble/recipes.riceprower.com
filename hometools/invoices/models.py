import datetime
import locale

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import escape_uri_path
from django.utils.functional import cached_property

from base_objects.models import ProjectBaseModel

from .managers import InvoiceManager, InvoiceItemLogManager


###################
## Custom fields ##
###################


class PhoneNumberField(models.CharField):
    description = "A phone number"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 20
        super().__init__(*args, **kwargs)


class CurrencyField(models.DecimalField):
    description = "An amount of currency, represented as a Decimal"

    def __init__(self, *args, **kwargs):
        kwargs["max_digits"] = 8
        kwargs["decimal_places"] = 2
        super().__init__(*args, **kwargs)


class HoursField(models.DecimalField):
    description = "A number of hours, represented as a Decimal"

    def __init__(self, *args, **kwargs):
        kwargs["max_digits"] = 6
        kwargs["decimal_places"] = 1
        validators = [MinValueValidator(0.0)]
        max_hours = kwargs.pop("max_hours", None)
        if max_hours:
            validators.append(MaxValueValidator(max_hours))
        kwargs["validators"] = validators
        super().__init__(*args, **kwargs)


###############
## Utilities ##
###############


def _google_map_search_url(address):
    """Given an address string, which is the raw output from an AddressField,
    return an escaped Google Maps search URL for that address.
    """
    output = address.replace("\r", "").replace("\n", " ")
    return escape_uri_path(f"https://www.google.com/maps/search/{output}")


def _address_fields_to_str(
    line1="", line2="", city="", state="", country="", zip_code=""
):
    output = line1
    if line2:
        output += f", {line2}"
    output += f", {city}, {state}"
    if country != "US":
        output += f", {country},"
    output += f" {zip_code}"
    return output


############
## Models ##
############


class Address(ProjectBaseModel):
    line_1 = models.CharField(max_length=255)
    line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    # TODO Redefine this
    STATE_CHOICES = (
        # Jerz on top
        ("NJ", "New Jersey"),
        # 50 states and DC plus Puerto Rico
        ("AK", "Alaska"),
        ("AL", "Alabama"),
        ("AR", "Arkansas"),
        ("AZ", "Arizona"),
        ("CA", "California"),
        ("CO", "Colorado"),
        ("CT", "Connecticut"),
        ("DC", "District of Columbia"),
        ("DE", "Delaware"),
        ("FL", "Florida"),
        ("GA", "Georgia"),
        ("HI", "Hawaii"),
        ("IA", "Iowa"),
        ("ID", "Idaho"),
        ("IL", "Illinois"),
        ("IN", "Indiana"),
        ("KS", "Kansas"),
        ("KY", "Kentucky"),
        ("LA", "Louisiana"),
        ("MA", "Massachusetts"),
        ("MD", "Maryland"),
        ("ME", "Maine"),
        ("MI", "Michigan"),
        ("MN", "Minnesota"),
        ("MO", "Missouri"),
        ("MS", "Mississippi"),
        ("MT", "Montana"),
        ("NB", "Nebraska"),
        ("NC", "North Carolina"),
        ("ND", "North Dakota"),
        ("NE", "Nebraska"),
        ("NH", "New Hampshire"),
        ("NM", "New Mexico"),
        ("NV", "Nevada"),
        ("NY", "New York"),
        ("OH", "Ohio"),
        ("OK", "Oklahoma"),
        ("OR", "Oregon"),
        ("PA", "Pennsylvania"),
        ("PR", "Puerto Rico"),
        ("RI", "Rhode Island"),
        ("SC", "South Carolina"),
        ("SD", "South Dakota"),
        ("TN", "Tennessee"),
        ("TX", "Texas"),
        ("UT", "Utah"),
        ("VA", "Virginia"),
        ("VT", "Vermont"),
        ("WA", "Washington"),
        ("WI", "Wisconsin"),
        ("WV", "West Virginia"),
        ("WY", "Wyoming"),
        # Other
        ("AA", "U.S. Armed Forces – Americas[d]"),
        ("AE", "U.S. Armed Forces – Europe[e]"),
        ("AP", "U.S. Armed Forces – Pacific[f]"),
        ("AS", "American Samoa"),
        ("CM", "Northern Mariana Islands"),
        ("CZ", "Panama Canal Zone"),
        ("FM", "Micronesia"),
        ("GU", "Guam"),
        ("MH", "Marshall Islands"),
        ("MP", "Northern Mariana Islands"),
        ("PI", "Philippine Islands"),
        ("PW", "Palau"),
        ("TT", "Trust Territory of the Pacific Islands"),
        ("VI", "U.S. Virgin Islands"),
    )
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default="NJ")
    country = models.CharField(max_length=5, default="US")
    zip_code = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "addresses"

    def __str__(self):
        return self.address_str

    @property
    def address_str(self):
        return _address_fields_to_str(
            self.line_1,
            self.line_2,
            self.city,
            self.state,
            self.country,
            self.zip_code,
        )

    @property
    def google_maps_url(self):
        return _google_map_search_url(self.address_str)


class UserProfile(ProjectBaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True
    )
    phone = PhoneNumberField(blank=True)

    def __str__(self):
        return self.user.username


class Client(ProjectBaseModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True
    )
    phone = PhoneNumberField(blank=True)

    def __str__(self):
        return self.name


class Project(ProjectBaseModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="projects"
    )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    billing_cycle = models.PositiveIntegerField(
        "Billing cycle recurrence (in days)", default=14
    )
    first_cycle_end_date = models.DateField(
        "Date of the end of the first billing cycle."
    )
    hourly_rate = CurrencyField("Rate per hour in $")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects"
    )

    def __str__(self):
        return self.name

    @cached_property
    def first_cycle_start_date(self):
        """Calculates the start date of the first billing cycle
        based on `first_cycle_end_date` and `billing_cycle`.

        As the end date minus one cycle is the same as the end date of a previous cycle,
        the start day of the next cycle is always the next day.
        So, the start date is one billing cycle prior, plus one day.

        Example:
          With a billing cycle of 7 days and first cycle ending on Sat, March 28, 2020;
          the first day of that cycle would be Sun, March 22, 2020.

          A simple -7 days would be March 21, which would be the end of
          a prior cycle that doesn't exist.
        """
        one_day = datetime.timedelta(days=1)
        return self.first_cycle_end_date - self.billing_cycle_delta + one_day

    @cached_property
    def billing_cycle_delta(self):
        """Returns a datetime.timedelta instance set to `self.billing_cycle` days."""
        return datetime.timedelta(days=self.billing_cycle)

    def _hourly_rate_str(self):
        locale.setlocale(locale.LC_ALL, "")
        return locale.currency(self.hourly_rate, grouping=True)

    _hourly_rate_str.short_description = hourly_rate.verbose_name
    hourly_rate_str = property(_hourly_rate_str)

    def billing_cycle_for_date(self, dt_):
        """Given a date/datetime object `dt_`, calculate the start and end dates
        of the billing cycle
        """
        if isinstance(dt_, datetime.datetime):
            dt_ = dt_.date()
        if not isinstance(dt_, datetime.date):
            raise ValueError("Must use a date or datetime object.")
        if dt_ <= self.first_cycle_start_date:
            raise ValueError("Date falls before the first billing cycle.")
        if self.end_date and dt_ > self.end_date:
            raise ValueError(
                "Cannot get billing range for a date after the ending date."
            )
        # Start checking in the billing cycle prior to first cycle's end date.
        cycle_end = self.first_cycle_end_date
        while cycle_end < dt_:
            # Increment by the delta each time so we check the next cycle(s)
            cycle_end += self.billing_cycle_delta
        # Here, we found the end of the billing cycle containing `dt_`.
        # Calculate the start of that cycle (subtract delta, add a day)
        cycle_start = cycle_end - self.billing_cycle_delta + datetime.timedelta(days=1)
        return cycle_start, cycle_end

    def curr_billing_cycle(self):
        """Return the date range of the current billing cycle, as of today."""
        return self.billing_cycle_for_date(timezone.localtime().date())

    def prev_billing_cycle(self):
        """Return the date range of the previous billing cycle.
        First gets the current billing cycle (`self.curr_billing_cycle`),
        then moves both dates back by one delta (`self.billing_cycle` number of days).
        """
        start_date, end_date = self.billing_cycle_for_date(timezone.localtime().date())
        if (end_date - self.billing_cycle_delta) < self.first_cycle_end_date:
            raise ValueError(
                (
                    "Current billing cycle is the first cycle for this Project: "
                    "no previous cycle available."
                )
            )
        return (
            start_date - self.billing_cycle_delta,
            end_date - self.billing_cycle_delta,
        )

    def generate_invoice(
        self, invoice_date, name=None, cycle_date=None, start_date=None, end_date=None
    ):
        """Creates a new Invoice for this project. `invoice_date` is required
        (saved as Invoice.invoice_date).

        If `name` is provided, uses that for the Invoice name;
        otherwise, a unique name is generated using the project name and invoice date.

        If `cycle_date` is provided as a date/datetime object,
        finds the regular billing cycle containing that date
        (using `billing_cycle_for_date`),
        then generates an invoice for that cycle date range.

        If `start_date` and `end_date` are provided,
        runs a custom Invoice for those dates in particular,
        even if they fall outside a normal billing cycle.

        If none of these dates are provided, the previous billing cycle
        is used as a default.

        Finally, returns the new invoice created.
        """
        if not any([cycle_date, start_date, end_date]):
            cycle_start, cycle_end = self.prev_billing_cycle()
        elif cycle_date:
            cycle_start, cycle_end = self.billing_cycle_for_date(cycle_date)
        elif not all([start_date, end_date]):
            raise ValueError(
                "`start_date` and `end_date` both required if one is provided"
            )
        else:
            cycle_start, cycle_end = start_date, end_date

        new_invoice = Invoice.objects.create(
            project=self,
            user=self.user,
            client=self.client,
            name=name,
            hourly_rate=self.hourly_rate,
            invoice_date=invoice_date,
            cycle_start_date=cycle_start,
            cycle_end_date=cycle_end,
        )
        new_invoice.gather_items()
        return new_invoice


class Item(ProjectBaseModel):
    """Definition for items that can be billed in the project."""

    NAME_MAXLENGTH = 50
    DESCRIPTION_MAXLENGTH = 255

    name = models.CharField(max_length=NAME_MAXLENGTH, unique=True, db_index=True)
    description = models.CharField(max_length=DESCRIPTION_MAXLENGTH, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="items")
    ITEM_TYPE_DEV = "DEV"
    ITEM_TYPE_SUPPORT = "SUPPORT"
    ITEM_TYPE_MAINTENANCE = "MAINT"
    ITEM_TYPE_OTHER = "OTHER"
    ITEM_TYPE_CHOICES = (
        (ITEM_TYPE_DEV, "Development"),
        (ITEM_TYPE_SUPPORT, "Support"),
        (ITEM_TYPE_MAINTENANCE, "Maintenance"),
        (ITEM_TYPE_OTHER, "Other"),
    )
    item_type = models.CharField(
        max_length=7, choices=ITEM_TYPE_CHOICES, default=ITEM_TYPE_DEV
    )
    ticket_number = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        output = f"{self.get_item_type_display()} - "
        if self.ticket_number:
            output += f"({self.ticket_number}) "
        output += self.name
        return output


class ItemLog(ProjectBaseModel):
    """An instance of an Item related to a date and number of hours worked."""

    objects = InvoiceItemLogManager()

    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    # Name, description, and project link preserved in case the Item is removed.
    _item_name = models.CharField(max_length=255, blank=True)
    _item_description = models.CharField(
        max_length=Item.DESCRIPTION_MAXLENGTH, blank=True
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="item_logs"
    )
    # Date and hours worked for this log.
    date = models.DateField()
    hours = HoursField(max_hours=24.0)

    def __str__(self):
        return (
            f"[{self.project.name}] {self.item_name} on {self.date}: {self.hours} hours"
        )

    def save(self, *args, **kwargs):  # pylint: disable=unused-argument,arguments-differ
        if self.item:
            # Store some identifying data from the item for historial records.
            self._item_name = str(self.item)
            self._item_description = self.item.description
            self.project = self.item.project
        super().save(*args, **kwargs)

    @cached_property
    def item_name(self):
        if self.item:
            return str(self.item)
        return self._item_name

    @cached_property
    def item_description(self):
        if self.item:
            return self.item.description
        return self._item_description


class Invoice(ProjectBaseModel):
    """A generated object containing copies of all relevant work data
    for historical records, showing all work performed within a specified timeframe,
    for whom, total billable hours, rates, and total invoiced amount.
    """

    objects = InvoiceManager()

    # Project details
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="project_invoices",
    )
    hourly_rate = CurrencyField("Rate per hour ($)")
    ## Historical copies
    _project_name = models.CharField("Project name", max_length=255, blank=True)

    # Client details
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_invoices",
    )
    ## Historical copies
    _client_name = models.CharField("Client name", max_length=255, blank=True)
    _client_address_line_1 = models.CharField(max_length=255, blank=True)
    _client_address_line_2 = models.CharField(max_length=255, blank=True)
    _client_address_city = models.CharField(max_length=255, blank=True)
    _client_address_state = models.CharField(
        max_length=2, choices=Address.STATE_CHOICES, default="NJ"
    )
    _client_address_country = models.CharField(max_length=5, default="US")
    _client_address_zip_code = models.CharField(max_length=10, blank=True)
    _client_phone = PhoneNumberField("Client phone", blank=True)

    # User
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_invoices"
    )

    # Invoice details
    name = models.CharField("Invoice name", max_length=255, unique=True, db_index=True)
    invoice_date = models.DateField()
    cycle_start_date = models.DateField("Invoiced from")
    cycle_end_date = models.DateField("Invoiced to")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if self.pk is None:
            # When first created, runs `new_name` using the provided name as a basis.
            # If no name has been provided, `new_name` will generate a default.
            self.name = self.new_name(base_name=self.name)
        if self.project:
            self._project_name = self.project.name
            if not self.client:
                self.client = self.project.client
        if self.client:
            self._client_name = self.client.name
            self._client_address_line_1 = self.client.new_address.line_1
            self._client_address_line_2 = self.client.new_address.line_2
            self._client_address_city = self.client.new_address.city
            self._client_address_state = self.client.new_address.state
            self._client_address_country = self.client.new_address.country
            self._client_address_zip_code = self.client.new_address.zip_code
            self._client_phone = self.client.phone

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("invoices:invoice-detail", kwargs={"pk": self.pk})

    @property
    def _client_address_str(self):
        return _address_fields_to_str(
            self._client_address_line_1,
            self._client_address_line_2,
            self._client_address_city,
            self._client_address_state,
            self._client_address_country,
            self._client_address_zip_code,
        )

    @cached_property
    def project_name(self):
        """Shorthand for the project name, returned either from the related Project
        or from the archived version.
        """
        if self.project:
            return self.project.name
        return self._project_name

    project_name.short_description = "project"

    @cached_property
    def client_name(self):
        """Shorthand for the client name, returned either from the related Client
        or from the archived version.
        """
        if self.client:
            return self.client.name
        return self._client_name

    client_name.short_description = "client"

    @cached_property
    def client_address(self):
        """Shorthand for the client address, returned either from the related Client
        or from the archived version.
        """
        if self.client:
            return self.client.address
        return self._client_address_str

    @cached_property
    def client_phone(self):
        """Shorthand for the client phone, returned either from the related Client
        or from the archived version.
        """
        if self.client:
            return self.client.phone
        return self._client_phone

    @property
    def total_hours(self):
        """Returns total number of hours from all invoice items
        attached to this Invoice.
        """
        return sum([x.total_hours for x in self.invoice_items.all()])

    @property
    def amount_billed(self):
        """Returns total amount of currency being billed to the Client
        on this invoice, as a function of the hourly rate and the total hours
        for all items attached to this Invoice.
        """
        return self.hourly_rate * self.total_hours

    @property
    def client_address_search_url(self):
        """Return a Google Maps search URL for the client address."""
        if self.client:
            return self.client.address.google_maps_url
        return _google_map_search_url(self._client_address_str)

    def _amount_billed_str(self):
        """Returns total amount of currency being billed to the Client
        on this invoice, as a function of the hourly rate and the total hours
        for all items attached to this Invoice.
        """
        locale.setlocale(locale.LC_ALL, "")
        return locale.currency(self.amount_billed, grouping=True)

    _amount_billed_str.short_description = "amount billed"
    amount_billed_str = property(_amount_billed_str)

    def _hourly_rate_str(self):
        locale.setlocale(locale.LC_ALL, "")
        return locale.currency(self.hourly_rate, grouping=True)

    _hourly_rate_str.short_description = hourly_rate.verbose_name
    hourly_rate_str = property(_hourly_rate_str)

    def _date_range_str(self):
        delta = self.cycle_end_date - self.cycle_start_date
        return (
            f"{self.cycle_start_date:%B %d, %Y} to {self.cycle_end_date:%B %d, %Y}\n"
            f"({delta.days + 1} day period)"
        ).replace(" 0", " ")

    _date_range_str.short_description = "invoice date range"
    date_range_str = property(_date_range_str)

    def new_name(self, base_name=None):
        """Creates and returns a new name for this Invoice,
        using `base_name` as a template if provided
        (or the project name and invoice date, if `base_name` is not provided).

        Since names must be unique, if a collision is detected with another Invoice,
        a version number will be appended, starting with "v02"
        and incrementing from there until a unique name is found.

        Be cautious using this on an existing Invoice in the database!
        This makes it more likely to have a name collision with itself,
        generating a "v02" name when it was not necessary.
        """
        inv_date = self.invoice_date
        if isinstance(self.invoice_date, datetime.datetime):
            # This can occur when the new name is being generated before
            # field validation converts a datetime to a date object,
            # causing `invoice_date` to include date information.
            inv_date = inv_date.date()  # pylint: disable=no-member

        name_template = base_name
        if not name_template:
            name_template = f"{self.project_name} {inv_date.isoformat()}"
        name = name_template
        version = 1
        while type(self).objects.filter(name=name).exists():
            version += 1
            name = f"{name_template} - v{version:0>2}"
        return name

    def clear_items(self):
        """Removes existing InvoiceItems and their associated InvoiceItemLogs
        from this Invoice.
        Useful prior to running `gather_items` to account for changes
        made to the live versions.
        """
        self.invoice_items.all().delete()

    def gather_items(self):
        """Copies ItemLogs and their related Item instances,
        which cover the same project and fit within the billing cycle
        covered by this invoice, into InvoiceItem and InvoiceItemLog instances
        connected with this Invoice.

        Basically, this is an archival action, that takes data from the live version
        of the system and maps it to the Invoice.
        """
        matching_item_logs = (
            ItemLog.objects.for_project(self.project)
            .within_cycle(self.cycle_start_date, self.cycle_end_date)
            .select_related("item")
        )
        item_log_cache = {}
        for log in matching_item_logs:
            invoice_item = item_log_cache.get(log.item.id)
            if invoice_item is None:
                invoice_item, _ = InvoiceItem.objects.get_or_create(
                    invoice=self,
                    _orig_item_id=log.item.id,
                    defaults={
                        "name": str(log.item),
                        "description": log.item.description,
                    },
                )
                item_log_cache[log.item.id] = invoice_item
            InvoiceItemLog.objects.get_or_create(
                invoice_item=invoice_item,
                _orig_log_id=log.id,
                defaults={
                    "date": log.date,
                    "hours": log.hours,
                },
            )


class InvoiceItem(ProjectBaseModel):
    """Essentially a copied version of an Item, related only to a specific Invoice."""

    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="invoice_items"
    )
    _orig_item_id = models.PositiveIntegerField()
    name = models.CharField(max_length=Item.NAME_MAXLENGTH)
    description = models.CharField(max_length=Item.DESCRIPTION_MAXLENGTH, blank=True)

    def __str__(self):
        return f"Invoice {self.invoice} / {self.name}"

    @cached_property
    def total_hours(self):
        return sum([x.hours for x in self.invoice_item_logs.all()])

    @cached_property
    def amount_billed(self):
        return sum([x.amount_billed for x in self.invoice_item_logs.all()])

    def _amount_billed_str(self):
        """Returns total amount of currency being billed to the Client
        on this invoice, as a function of the hourly rate and the total hours
        for all items attached to this Invoice.
        """
        locale.setlocale(locale.LC_ALL, "")
        return locale.currency(self.amount_billed, grouping=True)

    _amount_billed_str.short_description = "amount billed"
    amount_billed_str = property(_amount_billed_str)


class InvoiceItemLog(ProjectBaseModel):
    invoice_item = models.ForeignKey(
        InvoiceItem, on_delete=models.CASCADE, related_name="invoice_item_logs"
    )
    _orig_log_id = models.PositiveIntegerField()
    date = models.DateField()
    hours = HoursField(max_hours=24.0)

    def __str__(self):
        return f"Invoice {self.invoice_item} / {self.hours} hours on {self.date}"

    @cached_property
    def amount_billed(self):
        return self.hours * self.invoice_item.invoice.hourly_rate

    def _amount_billed_str(self):
        """Returns total amount of currency being billed to the Client
        on this invoice, as a function of the hourly rate and the total hours
        for all items attached to this Invoice.
        """
        locale.setlocale(locale.LC_ALL, "")
        return locale.currency(self.amount_billed, grouping=True)

    _amount_billed_str.short_description = "amount billed"
    amount_billed_str = property(_amount_billed_str)
