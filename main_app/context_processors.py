# context_processors.py
from .models import BrandSettings

def brand_settings(request):
    """Add brand settings to context for all templates"""
    if request.user.is_authenticated:
        try:
            settings = BrandSettings.objects.get(id=request.user)
        except BrandSettings.DoesNotExist:
            settings = None
    else:
        settings = None
    
    return {'brand_settings': settings}
