# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Invoice, InvoiceItem, InvoiceTemplate, TemplateItem, BrandSettings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, Button, HTML, Div

class BrandSettingsForm(forms.ModelForm):
    class Meta:
        model = BrandSettings
        fields = [
            'company_name', 'company_name_ar', 'company_email', 'company_phone',
            'company_address', 'company_address_ar', 'logo', 'logo_ar',
            'background_image', 'favicon', 'pdf_header_color', 'pdf_footer_color',
            'pdf_text_color', 'pdf_accent_color', 'invoice_footer_text',
            'invoice_footer_text_ar', 'invoice_terms', 'invoice_terms_ar',
            'show_logo', 'show_qr_code', 'decimal_places', 'currency_symbol'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'company_name_ar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم الشركة', 'dir': 'rtl'}),
            'company_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+973...'}),
            'company_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'company_address_ar': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'dir': 'rtl'}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'logo_ar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'background_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'favicon': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'pdf_header_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'pdf_footer_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'pdf_text_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'pdf_accent_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'invoice_footer_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'invoice_footer_text_ar': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'dir': 'rtl'}),
            'invoice_terms': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'invoice_terms_ar': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'dir': 'rtl'}),
            'show_logo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_qr_code': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'decimal_places': forms.NumberInput(attrs={'class': 'form-control', 'min': 2, 'max': 4}),
            'currency_symbol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'BHD'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_date', 'due_date', 'bill_to', 'bill_to_ar', 'mobile_number', 'email', 'tax_rate', 'discount_type', 'discount_value', 'notes', 'notes_ar']
        widgets = {
            'invoice_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bill_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'}),
            'bill_to_ar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم العميل', 'dir': 'rtl'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+973...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'tax_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100', 'placeholder': 'Tax %'}),
            'discount_type': forms.Select(attrs={'class': 'form-select'}),
            'discount_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes'}),
            'notes_ar': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'ملاحظات إضافية', 'dir': 'rtl'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['description', 'description_ar', 'quantity', 'price', 'unit', 'unit_ar']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Description'}),
            'description_ar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'وصف البند', 'dir': 'rtl'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'min': '0'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'min': '0'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit (Qty, Hour, Day)'}),
            'unit_ar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الوحدة', 'dir': 'rtl'}),
        }

class SearchInvoiceForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Search by invoice number, customer name, or mobile...',
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Status')] + list(Invoice.STATUS_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
