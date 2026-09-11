# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import random
import string
import uuid

class BrandSettings(models.Model):
    """Store company branding and PDF customization settings"""
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='brand_settings')
    company_name = models.CharField(max_length=200, default='GulfLimo')
    company_name_ar = models.CharField(max_length=200, default='ليمو الخليج')
    company_email = models.EmailField(default='info@gulflimo.com')
    company_phone = models.CharField(max_length=20, default='')
    company_address = models.TextField(default='')
    company_address_ar = models.TextField(default='')
    
    # Logo and images
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    logo_ar = models.ImageField(upload_to='logos/', null=True, blank=True, help_text='Logo for Arabic layouts')
    background_image = models.ImageField(upload_to='backgrounds/', null=True, blank=True)
    favicon = models.ImageField(upload_to='favicon/', null=True, blank=True)
    
    # PDF Customization
    pdf_header_color = models.CharField(max_length=7, default='#2c3e50', help_text='Hex color code')
    pdf_footer_color = models.CharField(max_length=7, default='#34495e', help_text='Hex color code')
    pdf_text_color = models.CharField(max_length=7, default='#333333', help_text='Hex color code')
    pdf_accent_color = models.CharField(max_length=7, default='#3498db', help_text='Hex color code')
    
    # Invoice customization
    invoice_footer_text = models.TextField(default='Thank you for your business!')
    invoice_footer_text_ar = models.TextField(default='شكراً على تعاملك معنا!')
    invoice_terms = models.TextField(default='Payment terms: Net 30', blank=True)
    invoice_terms_ar = models.TextField(default='شروط الدفع: خلال 30 يوم', blank=True)
    
    # Display settings
    show_logo = models.BooleanField(default=True)
    show_qr_code = models.BooleanField(default=True)
    decimal_places = models.IntegerField(default=3, validators=[MinValueValidator(2), MaxValueValidator(4)])
    currency_symbol = models.CharField(max_length=10, default='BHD')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Brand Settings'
        verbose_name_plural = 'Brand Settings'
    
    def __str__(self):
        return f'Brand Settings for {self.company_name}'

class Invoice(models.Model):
    """Enhanced invoice model with multilingual support"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('viewed', 'Viewed'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    invoice_date = models.DateField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)
    bill_to = models.CharField(max_length=200)
    bill_to_ar = models.CharField(max_length=200, blank=True)
    mobile_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    
    # Additional invoice fields
    invoice_from = models.CharField(max_length=200, default='GulfLimo')
    notes = models.TextField(blank=True)
    notes_ar = models.TextField(blank=True)
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    viewed_at = models.DateTimeField(null=True, blank=True)
    paid_date = models.DateField(null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    
    # Taxes and discounts
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    discount_type = models.CharField(max_length=10, choices=[('fixed', 'Fixed'), ('percent', 'Percentage')], default='fixed')
    discount_value = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['mobile_number']),
            models.Index(fields=['status']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        super().save(*args, **kwargs)
    
    def generate_invoice_number(self):
        count = Invoice.objects.filter(created_by=self.created_by).count() + 1
        sequential_part = f"{count:06d}"
        prefix = "GL"
        return f"{prefix}{sequential_part}"
    
    def subtotal(self):
        return sum(item.total() for item in self.items.all())
    
    def tax_amount(self):
        return (self.subtotal() * self.tax_rate) / 100
    
    def total_discount(self):
        if self.discount_type == 'fixed':
            return self.discount_value
        else:
            return (self.subtotal() * self.discount_value) / 100
    
    def total_amount(self):
        return self.subtotal() + self.tax_amount() - self.total_discount()
    
    def balance_due(self):
        return max(0, self.total_amount() - self.paid_amount)
    
    def is_overdue(self):
        return timezone.now().date() > self.due_date and self.status != 'paid'
    
    def __str__(self):
        return self.invoice_number

class InvoiceItem(models.Model):
    """Invoice line items with multilingual support"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    description_ar = models.CharField(max_length=300, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=3, default=1)
    price = models.DecimalField(max_digits=12, decimal_places=3)
    unit = models.CharField(max_length=50, default='Qty', blank=True)  # e.g., "Hour", "Day", etc.
    unit_ar = models.CharField(max_length=50, default='', blank=True)
    order = models.PositiveIntegerField(default=0)  # For ordering items
    
    class Meta:
        ordering = ['order', 'id']
    
    def total(self):
        return self.quantity * self.price
    
    def __str__(self):
        return self.description

class InvoiceTemplate(models.Model):
    """Save invoice templates for quick creation"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoice_templates')
    
    # Template data
    default_bill_to = models.CharField(max_length=200, blank=True)
    default_mobile = models.CharField(max_length=20, blank=True)
    default_email = models.EmailField(blank=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return self.name

class TemplateItem(models.Model):
    """Template line items"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(InvoiceTemplate, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=12, decimal_places=3)
    unit = models.CharField(max_length=50, default='Qty')
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.description

class ActivityLog(models.Model):
    """Track invoice activities and changes"""
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('viewed', 'Viewed'),
        ('edited', 'Edited'),
        ('sent', 'Sent'),
        ('paid', 'Marked as Paid'),
        ('cancelled', 'Cancelled'),
        ('pdf_generated', 'PDF Generated'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='activity_logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f'{self.get_action_display()} - {self.invoice.invoice_number}'
