from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from .models import Invoice, InvoiceItem, Receipt

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['status', 'student', 'session', 'term',  'class_for', 'balance_from_previous_term', 'payment_due']
        widgets = {
            'payment_due': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adding help text with URLs for session, term, student, and class_for fields
        self.fields['student'].help_text = mark_safe(
            '<a href="{}">Click here to add student</a>'.format(reverse_lazy('student-create')))
        self.fields['session'].help_text = mark_safe(
            '<a href="{}">Click here to add session</a>'.format(reverse_lazy('session-create')))
        self.fields['term'].help_text = mark_safe(
            '<a href="{}">Click here to add term</a>'.format(reverse_lazy('term-create')))
        self.fields['class_for'].help_text = mark_safe(
            '<a href="{}">Click here to add class</a>'.format(reverse_lazy('class-create')))

        self.fields['student'].empty_label = 'Select One student'
        self.fields['session'].empty_label = 'Select One session'
        self.fields['term'].empty_label = 'Select One term'
        self.fields['class_for'].empty_label = 'Select One class'

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