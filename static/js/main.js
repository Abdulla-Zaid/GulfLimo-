// static/js/main.js

// Dynamic invoice items
function addInvoiceItem() {
    const container = document.getElementById('items-container');
    const itemCount = container.children.length;
    
    const newItem = document.createElement('div');
    newItem.className = 'row mb-3 item-row';
    newItem.innerHTML = `
        <div class="col-md-4">
            <input type="text" name="description" class="form-control" placeholder="Description" required>
        </div>
        <div class="col-md-2">
            <input type="number" name="quantity" class="form-control" placeholder="Qty" value="1" min="0.001" step="0.001" required>
        </div>
        <div class="col-md-3">
            <input type="number" name="price" class="form-control" placeholder="Price" min="0" step="0.001" required>
        </div>
        <div class="col-md-2">
            <input type="text" name="unit" class="form-control" placeholder="Unit" value="Qty">
        </div>
        <div class="col-md-1">
            <button type="button" class="btn btn-danger btn-sm remove-item" onclick="removeInvoiceItem(this)">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;
    
    container.appendChild(newItem);
    attachRemoveListeners();
    calculateTotals();
}

function removeInvoiceItem(button) {
    const container = document.getElementById('items-container');
    if (container.children.length > 1) {
        button.closest('.item-row').remove();
        calculateTotals();
    } else {
        alert('At least one item is required');
    }
}

function attachRemoveListeners() {
    document.querySelectorAll('.remove-item').forEach(btn => {
        btn.onclick = function() { removeInvoiceItem(this); };
    });
}

function calculateTotals() {
    const items = [];
    document.querySelectorAll('.item-row').forEach(row => {
        const qty = parseFloat(row.querySelector('input[name="quantity"]').value) || 0;
        const price = parseFloat(row.querySelector('input[name="price"]').value) || 0;
        items.push({ qty, price });
    });
    
    const taxRate = parseFloat(document.querySelector('[name="tax_rate"]')?.value) || 0;
    const discountValue = parseFloat(document.querySelector('[name="discount_value"]')?.value) || 0;
    const discountType = document.querySelector('[name="discount_type"]')?.value || 'fixed';
    
    let subtotal = items.reduce((sum, item) => sum + (item.qty * item.price), 0);
    let tax = (subtotal * taxRate) / 100;
    let discount = discountType === 'fixed' ? discountValue : (subtotal * discountValue) / 100;
    let total = subtotal + tax - discount;
    
    // Update UI if elements exist
    const subtotalEl = document.getElementById('subtotal');
    const taxEl = document.getElementById('tax');
    const discountEl = document.getElementById('discount');
    const totalEl = document.getElementById('total');
    
    if (subtotalEl) subtotalEl.textContent = subtotal.toFixed(3);
    if (taxEl) taxEl.textContent = tax.toFixed(3);
    if (discountEl) discountEl.textContent = discount.toFixed(3);
    if (totalEl) totalEl.textContent = total.toFixed(3);
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    attachRemoveListeners();
    
    // Attach change listeners to calculate on change
    document.querySelectorAll('input[name="quantity"], input[name="price"], [name="tax_rate"], [name="discount_value"], [name="discount_type"]').forEach(el => {
        el.addEventListener('change', calculateTotals);
        el.addEventListener('input', calculateTotals);
    });
    
    calculateTotals();
});

// Toast notification
function showToast(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('.container-fluid').insertBefore(alertDiv, document.querySelector('.container-fluid').firstChild);
}
