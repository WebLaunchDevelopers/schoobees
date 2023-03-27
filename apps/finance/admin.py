from django.contrib import admin
from .models import Invoice, InvoiceItem, Receipt

class InvoiceAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name', 'roll_number', 'department')
    # list_display_links = ('id', 'name')
    # list_filter = ('department',)
    # search_fields = ('name', 'roll_number')
    class Meta:
        model = Invoice

class InvoiceItemAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name', 'roll_number', 'department')
    # list_display_links = ('id', 'name')
    # list_filter = ('department',)
    # search_fields = ('name', 'roll_number')
    class Meta:
        model = InvoiceItem

class ReceiptAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name', 'roll_number', 'department')
    # list_display_links = ('id', 'name')
    # list_filter = ('department',)
    # search_fields = ('name', 'roll_number')
    class Meta:
        model = Receipt

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem, InvoiceItemAdmin)
admin.site.register(Receipt, ReceiptAdmin)
