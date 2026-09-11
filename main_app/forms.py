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
        self.helper.layout = Layout(
            Fieldset('Company Information',
                Row(
                    Column('company_name', css_class='col-md-6'),
                    Column('company_name_ar', css_class='col-md-6'),
                ),
                Row(
                    Column('company_email', css_class='col-md-6'),
                    Column('company_phone', css_class='col-md-6'),
                ),
                Row(
                    Column('company_address', css_class='col-md-6'),
                    Column('company_address_ar', css_class='col-md-6'),
                ),
            ),
            Fieldset('Branding',
                Row(
                    Column('logo', css_class='col-md-6'),
                    Column('logo_ar', css_class='col-md-6'),
                ),
                Row(
                    Column('background_image', css_class='col-md-6'),
                    Column('favicon', css_class='col-md-6'),
                ),
            ),
            Fieldset('PDF Customization',
                Row(
                    Column('pdf_header_color', css_class='col-md-3'),
                    Column('pdf_footer_color', css_class='col-md-3'),
                    Column('pdf_text_color', css_class='col-md-3'),
                    Column('pdf_accent_color', css_class='col-md-3'),
                ),
            ),
            Fieldset('Invoice Settings',
                Row(
                    Column('invoice_footer_text', css_class='col-md-6'),
                    Column('invoice_footer_text_ar', css_class='col-md-6'),
                ),
                Row(
                    Column('invoice_terms', css_class='col-md-6'),
                    Column('invoice_terms_ar', css_class='col-md-6'),
                ),
                Row(
                    Column('currency_symbol', css_class='col-md-4'),
                    Column('decimal_places', css_class='col-md-4'),
                ),
                Row(
                    Column('show_logo', css_class='col-md-6'),
                    Column('show_qr_code', css_class='col-md-6'),
                ),
            ),
            Submit('submit', 'Save Settings', css_class='btn btn-primary btn-lg mt-4')
        )

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
        self.helper.layout = Layout(
            Fieldset('Invoice Information',
                Row(
                    Column('invoice_date', css_class='col-md-4'),
                    Column('due_date', css_class='col-md-4'),
                    Column('tax_rate', css_class='col-md-4'),
                ),
                Row(
                    Column('bill_to', css_class='col-md-6'),
                    Column('bill_to_ar', css_class='col-md-6'),
                ),
                Row(
                    Column('mobile_number', css_class='col-md-6'),
                    Column('email', css_class='col-md-6'),
                ),
                Row(
                    Column('discount_type', css_class='col-md-6'),
                    Column('discount_value', css_class='col-md-6'),
                ),
                Row(
                    Column('notes', css_class='col-md-6'),
                    Column('notes_ar', css_class='col-md-6'),
                ),
            ),
        )

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

class InvoiceTemplateForm(forms.ModelForm):
    class Meta:
        model = InvoiceTemplate
        fields = ['name', 'description', 'default_bill_to', 'default_mobile', 'default_email', 'tax_rate', 'is_default']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'default_bill_to': forms.TextInput(attrs={'class': 'form-control'}),
            'default_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'default_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tax_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TemplateItemForm(forms.ModelForm):
    class Meta:
        model = TemplateItem
        fields = ['description', 'price', 'unit']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'min': '0'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit'}),
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
