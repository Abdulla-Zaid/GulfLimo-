# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Invoice Management
    path('create/', views.create_invoice, name='create_invoice'),
    path('invoice/<uuid:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/<uuid:invoice_id>/edit/', views.edit_invoice, name='edit_invoice'),
    path('invoice/<uuid:invoice_id>/mark-paid/', views.mark_as_paid, name='mark_as_paid'),
    path('invoice/<uuid:invoice_id>/cancel/', views.cancel_invoice, name='cancel_invoice'),
    
    # PDF Generation
    path('invoice/<uuid:invoice_id>/pdf/', views.generate_pdf, name='generate_pdf'),
    path('invoice/<uuid:invoice_id>/pdf/<str:language>/', views.generate_pdf, name='generate_pdf_lang'),
    
    # Search & Filtering
    path('search/', views.search_invoices, name='search_invoices'),
    
    # Brand Settings
    path('settings/brand/', views.brand_settings, name='brand_settings'),
    
    # API Endpoints
    path('api/invoice/<uuid:invoice_id>/preview/', views.api_invoice_preview, name='api_invoice_preview'),
    path('api/calculate-totals/', views.api_calculate_totals, name='api_calculate_totals'),
]
