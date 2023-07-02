from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from .models import Invoice, InvoiceItem, Receipt
from apps.corecode.models import AcademicSession, AcademicTerm, Subject, StudentClass
from apps.students.models import Student

class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ['status', 'student', 'class_for', 'balance_from_previous_term', 'payment_due']
        widgets = {
            'payment_due': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args,user=None ,**kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Adding help text with URLs for session, term, student, and class_for fields
            self.fields['student'].help_text = mark_safe(
                '<a href="{}">Click here to add student</a>'.format(reverse_lazy('student-create')))
            self.fields['class_for'].help_text = mark_safe(
                '<a href="{}">Click here to add class</a>'.format(reverse_lazy('class-create')))

            self.fields['student'].empty_label = 'Select One student'
            self.fields['class_for'].empty_label = 'Select One class'

            self.fields['student'].queryset = Student.objects.filter(user=user)
            self.fields['class_for'].queryset = StudentClass.objects.filter(user=user)

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