"""Views for invoices app."""

# from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Invoice


@method_decorator(permission_required("invoices.add_invoice"), name="dispatch")
class InvoiceListView(ListView):
    queryset = Invoice.objects.order_by("-invoice_date")
    context_object_name = "invoices"
    paginate_by = 10


@method_decorator(permission_required("invoices.add_invoice"), name="dispatch")
class InvoiceDetailView(DetailView):
    model = Invoice
    context_object_name = "invoice"
