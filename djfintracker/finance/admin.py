from django.contrib import admin
from .models import Transaction,Goal
from import_export import resources
from import_export.admin import ExportMixin


class transactionsresournce(resources.ModelResource):
    class meta:
        model = Transaction
        fields = ('date', 'title', 'amount', 'Transaction_type')

class transactionAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = transactionsresournce        
    fields = ('date', 'title', 'amount', 'Transaction_type')
    scarch_fields = ('title',)

# Register your models here.

admin.site.register(Transaction , transactionAdmin)
admin.site.register(Goal)
