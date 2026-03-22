# hr_vault/forms.py

from django import forms
from .models import EmployeeRecord

class EmployeeRecordForm(forms.ModelForm):
    """
    Form for creating/updating employee records
    """
    
    # Explicitly declare fields to ensure they're editable
    bank_account_number = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234567890'
        }),
        required=True,
        help_text="Bank account number (will be encrypted)"
    )
    
    annual_salary = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '75000.00',
            'step': '0.01'
        }),
        required=True,
        help_text="Annual salary (will be encrypted)"
    )
    
    class Meta:
        model = EmployeeRecord
        fields = ['employee_name', 'department', 'bank_account_number', 'annual_salary']
        exclude = ['added_by']
        widgets = {
            'employee_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Engineering'
            }),
        }

    def clean_annual_salary(self):
        """Validate salary is a positive number"""
        salary = self.cleaned_data.get('annual_salary')
        if salary:
            try:
                salary_float = float(salary)
                if salary_float <= 0:
                    raise forms.ValidationError("Salary must be a positive number")
                return salary_float
            except (ValueError, TypeError):
                raise forms.ValidationError("Please enter a valid salary amount")
        return salary
    
    def clean_bank_account_number(self):
        """Validate bank account number"""
        bank_account = self.cleaned_data.get('bank_account_number')
        if bank_account:
            # Remove any spaces or dashes
            bank_account = ''.join(bank_account.split())
            if len(bank_account) < 5:
                raise forms.ValidationError("Please enter a valid bank account number")
        return bank_account
