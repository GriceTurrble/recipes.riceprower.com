from django.urls import path

from . import views

app_name = "invoices"
urlpatterns = [
    path("", views.InvoiceListView.as_view(), name="invoice-list"),
    path("<int:pk>/", views.InvoiceDetailView.as_view(), name="invoice-detail"),
]
