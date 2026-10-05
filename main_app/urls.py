# urls.py (app-level)
from django.urls import path
from .import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_invoice, name='create_invoice'),
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/<int:invoice_id>/edit/', views.edit_invoice, name='edit_invoice'),
    path('search/', views.search_invoices, name='search_invoices'),
    path('invoice/<int:invoice_id>/pdf/', views.generate_pdf, name='generate_pdf'),
]