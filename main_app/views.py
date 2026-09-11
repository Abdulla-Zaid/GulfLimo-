# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.db.models import Q, Sum, Count
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
import base64
import os
import qrcode
from io import BytesIO
from decimal import Decimal

try:
    from xhtml2pdf import pisa
except ImportError:
    pisa = None

from .models import Invoice, InvoiceItem, BrandSettings, ActivityLog, InvoiceTemplate
from .forms import InvoiceForm, InvoiceItemForm, SearchInvoiceForm, BrandSettingsForm
from .utils import get_brand_settings, log_activity

# ==================== Dashboard & Analytics ====================

@login_required
def dashboard(request):
    """Main dashboard with analytics"""
    user = request.user
    invoices = Invoice.objects.filter(created_by=user)
    
    # Calculate statistics
    total_invoices = invoices.count()
    total_revenue = sum(inv.total_amount() for inv in invoices if inv.status == 'paid')
    pending_amount = sum(inv.balance_due() for inv in invoices if inv.status in ['sent', 'viewed', 'partially_paid'])
    overdue_count = invoices.filter(status='overdue').count()
    
    # Recent invoices
    recent_invoices = invoices[:5]
    
    context = {
        'total_invoices': total_invoices,
        'total_revenue': total_revenue,
        'pending_amount': pending_amount,
        'overdue_count': overdue_count,
        'recent_invoices': recent_invoices,
    }
    
    return render(request, 'gulflimo/dashboard.html', context)

# ==================== Invoice Management ====================

@login_required
def create_invoice(request):
    """Create new invoice with dynamic items"""
    brand_settings = get_brand_settings(request.user)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()
            
            # Process items
            descriptions = request.POST.getlist('description')
            descriptions_ar = request.POST.getlist('description_ar')
            quantities = request.POST.getlist('quantity')
            prices = request.POST.getlist('price')
            units = request.POST.getlist('unit')
            units_ar = request.POST.getlist('unit_ar')
            
            for i in range(len(descriptions)):
                if descriptions[i]:
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        description=descriptions[i],
                        description_ar=descriptions_ar[i] if i < len(descriptions_ar) else '',
                        quantity=Decimal(quantities[i]) if quantities[i] else 1,
                        price=Decimal(prices[i]) if prices[i] else 0,
                        unit=units[i] if i < len(units) else 'Qty',
                        unit_ar=units_ar[i] if i < len(units_ar) else '',
                        order=i
                    )
            
            log_activity(invoice, request.user, 'created', 'Invoice created', request)
            messages.success(request, 'Invoice created successfully!')
            return redirect('invoice_detail', invoice_id=invoice.id)
    else:
        form = InvoiceForm()
    
    context = {
        'form': form,
        'brand_settings': brand_settings,
    }
    return render(request, 'gulflimo/create_invoice.html', context)

@login_required
def invoice_detail(request, invoice_id):
    """View invoice details"""
    invoice = get_object_or_404(Invoice, id=invoice_id, created_by=request.user)
    brand_settings = get_brand_settings(request.user)
    activity_logs = invoice.activity_logs.all()[:10]
    
    # Mark as viewed if not already
    if not invoice.viewed_at:
        invoice.viewed_at = timezone.now()
        invoice.save()
        log_activity(invoice, request.user, 'viewed', 'Invoice viewed', request)
    
    context = {
        'invoice': invoice,
        'brand_settings': brand_settings,
        'activity_logs': activity_logs,
    }
    return render(request, 'gulflimo/invoice_detail.html', context)

@login_required
def edit_invoice(request, invoice_id):
    """Edit invoice and items"""
    invoice = get_object_or_404(Invoice, id=invoice_id, created_by=request.user)
    brand_settings = get_brand_settings(request.user)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            
            # Delete existing items
            invoice.items.all().delete()
            
            # Add new items
            descriptions = request.POST.getlist('description')
            descriptions_ar = request.POST.getlist('description_ar')
            quantities = request.POST.getlist('quantity')
            prices = request.POST.getlist('price')
            units = request.POST.getlist('unit')
            units_ar = request.POST.getlist('unit_ar')
            
            for i in range(len(descriptions)):
                if descriptions[i]:
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        description=descriptions[i],
                        description_ar=descriptions_ar[i] if i < len(descriptions_ar) else '',
                        quantity=Decimal(quantities[i]) if quantities[i] else 1,
                        price=Decimal(prices[i]) if prices[i] else 0,
                        unit=units[i] if i < len(units) else 'Qty',
                        unit_ar=units_ar[i] if i < len(units_ar) else '',
                        order=i
                    )
            
            log_activity(invoice, request.user, 'edited', 'Invoice edited', request)
            messages.success(request, 'Invoice updated successfully!')
            return redirect('invoice_detail', invoice_id=invoice.id)
    else:
        form = InvoiceForm(instance=invoice)
    
    items = invoice.items.all()
    context = {
        'form': form,
        'invoice': invoice,
        'items': items,
        'brand_settings': brand_settings,
    }
    return render(request, 'gulflimo/edit_invoice.html', context)

# ==================== Search & Filtering ====================

@login_required
def search_invoices(request):
    """Advanced search with filters"""
    form = SearchInvoiceForm(request.GET or None)
    invoices = Invoice.objects.filter(created_by=request.user)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        status = form.cleaned_data.get('status')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        
        if query:
            invoices = invoices.filter(
                Q(invoice_number__icontains=query) |
                Q(bill_to__icontains=query) |
                Q(mobile_number__icontains=query)
            )
        
        if status:
            invoices = invoices.filter(status=status)
        
        if date_from:
            invoices = invoices.filter(invoice_date__gte=date_from)
        
        if date_to:
            invoices = invoices.filter(invoice_date__lte=date_to)
    
    context = {
        'form': form,
        'invoices': invoices,
        'count': invoices.count(),
    }
    return render(request, 'gulflimo/search.html', context)

# ==================== Invoice Status ====================

@login_required
@require_POST
def mark_as_paid(request, invoice_id):
    """Mark invoice as paid"""
    invoice = get_object_or_404(Invoice, id=invoice_id, created_by=request.user)
    paid_amount = request.POST.get('paid_amount')
    
    if paid_amount:
        invoice.paid_amount = Decimal(paid_amount)
        invoice.paid_date = timezone.now().date()
        invoice.status = 'paid' if invoice.paid_amount >= invoice.total_amount() else 'partially_paid'
        invoice.save()
        
        log_activity(invoice, request.user, 'paid', f'Marked as paid: {paid_amount}', request)
        messages.success(request, 'Invoice marked as paid!')
    
    return redirect('invoice_detail', invoice_id=invoice.id)

@login_required
@require_POST
def cancel_invoice(request, invoice_id):
    """Cancel invoice"""
    invoice = get_object_or_404(Invoice, id=invoice_id, created_by=request.user)
    invoice.status = 'cancelled'
    invoice.save()
    
    log_activity(invoice, request.user, 'cancelled', 'Invoice cancelled', request)
    messages.success(request, 'Invoice cancelled!')
    
    return redirect('invoice_detail', invoice_id=invoice.id)

# ==================== PDF Generation ====================

@login_required
def generate_pdf(request, invoice_id, language='en'):
    """Generate customized PDF"""
    invoice = get_object_or_404(Invoice, id=invoice_id, created_by=request.user)
    brand_settings = get_brand_settings(request.user)
    
    template_path = 'gulflimo/invoice_pdf.html'
    
    # Prepare images as base64
    logo_base64 = None
    background_base64 = None
    
    if brand_settings.logo:
        try:
            with open(brand_settings.logo.path, "rb") as image_file:
                logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')
                logo_base64 = f"data:image/png;base64,{logo_base64}"
        except (FileNotFoundError, AttributeError):
            logo_base64 = None
    
    if brand_settings.background_image:
        try:
            with open(brand_settings.background_image.path, "rb") as image_file:
                background_base64 = base64.b64encode(image_file.read()).decode('utf-8')
                background_base64 = f"data:image/jpeg;base64,{background_base64}"
        except (FileNotFoundError, AttributeError):
            background_base64 = None
    
    # Generate QR code if enabled
    qr_code_base64 = None
    if brand_settings.show_qr_code:
        qr = qrcode.QRCode(version=1, box_size=4, border=1)
        qr.add_data(f"Invoice: {invoice.invoice_number}")
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_code_base64 = base64.b64encode(qr_buffer.getvalue()).decode('utf-8')
        qr_code_base64 = f"data:image/png;base64,{qr_code_base64}"
    
    context = {
        'invoice': invoice,
        'brand_settings': brand_settings,
        'logo_base64': logo_base64,
        'background_base64': background_base64,
        'qr_code_base64': qr_code_base64,
        'language': language,
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    if pisa is not None:
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error generating PDF')
        
        log_activity(invoice, request.user, 'pdf_generated', 'PDF generated', request)
        return response
    else:
        return HttpResponse('PDF generation is not available')

# ==================== Brand Settings ====================

@login_required
def brand_settings(request):
    """Manage brand and PDF customization settings"""
    try:
        settings = BrandSettings.objects.get(id=request.user)
    except BrandSettings.DoesNotExist:
        settings = BrandSettings.objects.create(id=request.user)
    
    if request.method == 'POST':
        form = BrandSettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand settings updated successfully!')
            return redirect('brand_settings')
    else:
        form = BrandSettingsForm(instance=settings)
    
    context = {'form': form, 'settings': settings}
    return render(request, 'gulflimo/brand_settings.html', context)

# ==================== AJAX API ====================

@login_required
def api_invoice_preview(request, invoice_id):
    """API endpoint for invoice preview"""
    invoice = get_object_or_404(Invoice, id=invoice_id, created_by=request.user)
    brand_settings = get_brand_settings(request.user)
    
    data = {
        'invoice_number': invoice.invoice_number,
        'bill_to': invoice.bill_to,
        'mobile_number': invoice.mobile_number,
        'subtotal': float(invoice.subtotal()),
        'tax_amount': float(invoice.tax_amount()),
        'discount': float(invoice.total_discount()),
        'total': float(invoice.total_amount()),
        'balance_due': float(invoice.balance_due()),
        'status': invoice.status,
    }
    return JsonResponse(data)

@login_required
def api_calculate_totals(request):
    """Calculate invoice totals dynamically"""
    if request.method == 'POST':
        items_data = request.POST.getlist('items')
        tax_rate = Decimal(request.POST.get('tax_rate', 0))
        discount_value = Decimal(request.POST.get('discount_value', 0))
        discount_type = request.POST.get('discount_type', 'fixed')
        
        subtotal = Decimal(0)
        for item in items_data:
            qty, price = item.split(',')
            subtotal += Decimal(qty) * Decimal(price)
        
        tax = (subtotal * tax_rate) / 100
        discount = discount_value if discount_type == 'fixed' else (subtotal * discount_value) / 100
        total = subtotal + tax - discount
        
        return JsonResponse({
            'subtotal': float(subtotal),
            'tax': float(tax),
            'discount': float(discount),
            'total': float(total),
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
