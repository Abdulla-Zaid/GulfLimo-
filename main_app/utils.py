# utils.py
from .models import BrandSettings, ActivityLog
from django.core.exceptions import ObjectDoesNotExist

def get_brand_settings(user):
    """Get or create brand settings for user"""
    try:
        return BrandSettings.objects.get(id=user)
    except ObjectDoesNotExist:
        return BrandSettings.objects.create(id=user)

def log_activity(invoice, user, action, description='', request=None):
    """Log invoice activity"""
    ip_address = None
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
    
    ActivityLog.objects.create(
        invoice=invoice,
        user=user,
        action=action,
        description=description,
        ip_address=ip_address,
    )
