from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import (
    Address,
    Client,
    Invoice,
    InvoiceItem,
    InvoiceItemLog,
    Item,
    ItemLog,
    Project,
    UserProfile,
)

User = get_user_model()  # pylint: disable=invalid-name


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = "user"
    can_delete = False
    verbose_plural_name = "Profile"
    # fmt: off
    # ^ Fieldsets are a lot easier to read when they're not smushed.
    fieldsets = (
        (None, {
            "fields": ("address", "phone"),
        }),
    )
    # fmt: on


admin.site.unregister(User)


@admin.register(User)
class ProfileUserAdmin(UserAdmin):
    def add_view(self, request, form_url="", extra_context=None):
        self.inlines = []
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.inlines = [
            UserProfileInline,
        ]
        return super().change_view(request, object_id, form_url, extra_context)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "ticket_number",
        "project",
        "item_type",
    )


@admin.register(ItemLog)
class ItemLogAdmin(admin.ModelAdmin):
    fields = (
        "item",
        "date",
        "hours",
    )
    list_filter = ("date", "project")
    list_display = (
        "date",
        "hours",
        "item_name",
        "project",
    )
    list_display_links = ("item_name",)


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem

    fields = (
        "name",
        "total_hours",
        "amount_billed_str",
    )
    readonly_fields = (
        "name",
        "total_hours",
        "amount_billed_str",
    )
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    date_hierarchy = "invoice_date"
    # fmt: off
    fieldsets = (
        ("Invoice details", {
            "fields": (
                "name",
                "invoice_date",
                "invoice_date_range",
                "total_hours",
                "hourly_rate_str",
                "amount_billed_str",
            )
        }),
        ("Billed to", {
            "fields": (
                "project_name",
                "client_details",
            )
        }),
    )
    # fmt: on
    readonly_fields = (
        "amount_billed_str",
        "client_address",
        "client_details",
        "cycle_end_date",
        "cycle_start_date",
        "hourly_rate_str",
        "invoice_date_range",
        "invoice_date",
        "project_name",
        "total_hours",
    )
    inlines = [InvoiceItemInline]

    def client_details(self, obj):
        address = obj.client_address.replace("\r", "").replace("\n", ", ")
        link = f"<a href='{obj.client_address_search_url}' target='_blank'>(Map)</a>"
        phone = (
            f"({obj.client_phone[:3]}) {obj.client_phone[3:6]}-{obj.client_phone[6:]}"
        )
        return mark_safe(
            (
                f"<strong>{obj.client_name}</strong><br/>"
                f"{address} {link}<br/>"
                f"{phone}"
            )
        )

    def invoice_date_range(self, obj):
        delta = obj.cycle_end_date - obj.cycle_start_date
        return (
            f"{obj.cycle_start_date:%B %d, %Y} to {obj.cycle_end_date:%B %d, %Y}\n"
            f"({delta.days + 1} day period)"
        ).replace(" 0", " ")

    client_details.short_description = "client"


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    pass


@admin.register(InvoiceItemLog)
class InvoiceItemLogAdmin(admin.ModelAdmin):
    pass
