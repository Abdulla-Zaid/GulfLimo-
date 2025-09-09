# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Q  # Add this import
import base64
import os
from django.conf import settings
from io import BytesIO
try:
    from xhtml2pdf import pisa
except ImportError:
    pisa = None
    print("xhtml2pdf is not installed. PDF generation will not work.")

from .models import Invoice, InvoiceItem
from .forms import InvoiceForm, InvoiceItemForm

@login_required
def dashboard(request):
    return render(request, 'gulflimo/dashboard.html')

@login_required
def create_invoice(request):
    if request.method == 'POST':
        # Create form without invoice_number since it will be auto-generated
        invoice_form = InvoiceForm(request.POST)
        if invoice_form.is_valid():
            invoice = invoice_form.save(commit=False)
            invoice.created_by = request.user
            # invoice_number will be auto-generated in the save() method
            invoice.save()
            
            # Process items
            descriptions = request.POST.getlist('description')
            quantities = request.POST.getlist('quantity')
            prices = request.POST.getlist('price')
            
            for i in range(len(descriptions)):
                if descriptions[i]:  # Only save if description exists
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        description=descriptions[i],
                        quantity=int(quantities[i]),
                        price=float(prices[i])
                    )
            
            return redirect('invoice_detail', invoice_id=invoice.id)
    else:
        invoice_form = InvoiceForm()
    
    return render(request, 'gulflimo/create_invoice.html', {'form': invoice_form})

@login_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'gulflimo/invoice_detail.html', {'invoice': invoice})

@login_required
def search_invoices(request):
    query = request.GET.get('q')
    invoices = []
    
    if query:
        # Use Q objects for complex queries
        invoices = Invoice.objects.filter(
            Q(invoice_number__icontains=query) | 
            Q(mobile_number__icontains=query)
        )
    
    return render(request, 'gulflimo/search.html', {'invoices': invoices, 'query': query})

@login_required


@login_required
def edit_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if request.method == 'POST':
        # Update invoice details
        invoice_form = InvoiceForm(request.POST, instance=invoice)
        if invoice_form.is_valid():
            invoice_form.save()
            
            # Delete existing items
            invoice.items.all().delete()
            
            # Add new items
            descriptions = request.POST.getlist('description')
            quantities = request.POST.getlist('quantity')
            prices = request.POST.getlist('price')
            
            for i in range(len(descriptions)):
                if descriptions[i]:  # Only save if description exists
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        description=descriptions[i],
                        quantity=int(quantities[i]),
                        price=float(prices[i])
                    )
            
            return redirect('invoice_detail', invoice_id=invoice.id)
    else:
        invoice_form = InvoiceForm(instance=invoice)
    
    # Get existing items for the form
    items = invoice.items.all()
    
    return render(request, 'gulflimo/edit_invoice.html', {
        'form': invoice_form,
        'invoice': invoice,
        'items': items
    })

@login_required
def generate_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    template_path = 'gulflimo/invoice_pdf.html'
    
    # Generate base64 strings for images
    logo_base64 = None
    background_base64 = None
    
    # Logo path
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
    try:
        with open(logo_path, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')
            logo_base64 = f"data:image/png;base64,{logo_base64}"
    except FileNotFoundError:
        logo_base64 = None
    
    # Background path
    background_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'background.jpg')
    try:
        with open(background_path, "rb") as image_file:
            background_base64 = base64.b64encode(image_file.read()).decode('utf-8')
            background_base64 = f"data:image/jpeg;base64,{background_base64}"
    except FileNotFoundError:
        background_base64 = None
    
    context = {
        'invoice': invoice,
        'logo_base64': logo_base64,
        'background_base64': background_base64,
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    if pisa is not None:
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        return HttpResponse('PDF generation is not available. Please install xhtml2pdf.')