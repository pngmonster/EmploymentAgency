from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ('employer', 'amount', 'status', 'created_at')
    list_filter   = ('status',)
    search_fields = ('employer__company_name',)
    readonly_fields = ('applications_snapshot', 'created_at', 'updated_at')
