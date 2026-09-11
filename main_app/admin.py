# admin.py
from django.contrib import admin
from .models import Invoice, InvoiceItem, BrandSettings, InvoiceTemplate, TemplateItem, ActivityLog

@admin.register(BrandSettings)
class BrandSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Company Information', {
            'fields': ('company_name', 'company_name_ar', 'company_email', 'company_phone', 'company_address', 'company_address_ar')
        }),
        ('Branding', {
            'fields': ('logo', 'logo_ar', 'background_image', 'favicon')
        }),
        ('PDF Customization', {
            'fields': ('pdf_header_color', 'pdf_footer_color', 'pdf_text_color', 'pdf_accent_color')
        }),
        ('Invoice Settings', {
            'fields': ('invoice_footer_text', 'invoice_footer_text_ar', 'invoice_terms', 'invoice_terms_ar', 'show_logo', 'show_qr_code', 'decimal_places', 'currency_symbol')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    fields = ('description', 'description_ar', 'quantity', 'price', 'unit')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'bill_to', 'invoice_date', 'status', 'total_amount', 'created_by')
    list_filter = ('status', 'invoice_date', 'created_at')
    search_fields = ('invoice_number', 'bill_to', 'mobile_number')
    readonly_fields = ('invoice_number', 'created_at', 'updated_at', 'viewed_at')
    inlines = [InvoiceItemInline]
    fieldsets = (
        ('Invoice Information', {
            'fields': ('invoice_number', 'invoice_date', 'due_date', 'status')
        }),
        ('Customer Details', {
            'fields': ('bill_to', 'bill_to_ar', 'mobile_number', 'email')
        }),
        ('Charges', {
            'fields': ('tax_rate', 'discount_type', 'discount_value')
        }),
        ('Payment', {
            'fields': ('paid_date', 'paid_amount')
        }),
        ('Notes', {
            'fields': ('notes', 'notes_ar')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at', 'viewed_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'action', 'user', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('invoice__invoice_number', 'user__username')
    readonly_fields = ('id', 'timestamp')
