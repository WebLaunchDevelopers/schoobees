from django.contrib import admin
from .models import Invoice, InvoiceItem, Receipt


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'term', 'class_for', 'balance', 'status')
    search_fields = ('student__first_name', 'student__last_name')
    list_filter = ('session', 'term', 'class_for', 'status')
    readonly_fields = ('balance',)
    ordering = ('student', 'term')


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'description', 'amount')
    list_filter = ('invoice__session', 'invoice__term', 'invoice__class_for')


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount_paid', 'date_paid')
    search_fields = ('invoice__student__first_name', 'invoice__student__last_name')
    list_filter = ('invoice__session', 'invoice__term', 'invoice__class_for')
