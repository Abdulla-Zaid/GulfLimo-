# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    invoice_date = models.DateField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)
    bill_to = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=20)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate invoice number only if it doesn't exist
            self.invoice_number = self.generate_invoice_number()
        super().save(*args, **kwargs)
    
    def generate_invoice_number(self):
        # Get the count of existing invoices to generate sequential number
        count = Invoice.objects.count() + 1
        # Format as a 6-digit number with leading zeros
        sequential_part = f"{count:06d}"
        
        # You can add a prefix if you want (e.g., GL for GulfLimo)
        prefix = "GL"
        
        # Combine prefix and sequential number
        return f"{prefix}{sequential_part}"
    
    def total_amount(self):
        return sum(item.total() for item in self.items.all())
    
    def __str__(self):
        return self.invoice_number

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def total(self):
        return self.quantity * self.price
    
    def __str__(self):
        return self.description