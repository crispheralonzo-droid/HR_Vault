# hr_vault/admin.py

from django.contrib import admin
from django import forms
from .models import EmployeeRecord

class EmployeeRecordAdminForm(forms.ModelForm):
    """Custom admin form to handle encrypted fields"""
    
    bank_account_number = forms.CharField(
        widget=forms.TextInput(attrs={'size': '40'})
    )
    
    annual_salary = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'size': '20'})
    )
    
    class Meta:
        model = EmployeeRecord
        fields = '__all__'

class EmployeeRecordAdmin(admin.ModelAdmin):
    form = EmployeeRecordAdminForm
    list_display = ['employee_name', 'department', 'get_bank_account_display', 'get_salary_display', 'added_by', 'created_at']
    list_filter = ['department', 'added_by', 'created_at']
    search_fields = ['employee_name', 'department']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_bank_account_display(self, obj):
        return obj.get_bank_account_display()
    get_bank_account_display.short_description = 'Bank Account (Masked)'
    
    def get_salary_display(self, obj):
        return obj.get_salary_display()
    get_salary_display.short_description = 'Salary'
    
    def save_model(self, request, obj, form, change):
        """Override save_model to ensure added_by is set"""
        if not obj.pk:  # If this is a new object
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('employee_name', 'department')
        }),
        ('Sensitive Financial Data (Will be encrypted)', {
            'fields': ('bank_account_number', 'annual_salary'),
            'classes': ('wide',)
        }),
        ('Audit Information', {
            'fields': ('added_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(EmployeeRecord, EmployeeRecordAdmin)