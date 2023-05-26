from django import forms
from django.forms import inlineformset_factory, modelformset_factory

from .models import Invoice, InvoiceItem, Receipt

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['status', 'student', 'session', 'term',  'class_for', 'balance_from_previous_term', 'payment_due']
        widgets = {
            'payment_due': forms.DateInput(attrs={'type': 'date'}),
        }

InvoiceItemFormset = inlineformset_factory(
    Invoice, InvoiceItem, fields=["description", "amount"], extra=1, can_delete=True
)

InvoiceReceiptFormSet = inlineformset_factory(
    Invoice,
    Receipt,
    fields=("amount_paid", "date_paid", "payment_method", "comment"),
    extra=0,
    can_delete=True,
)

Invoices = modelformset_factory(Invoice, form=InvoiceForm, extra=4)