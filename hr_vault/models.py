from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings
import base64
import os

# Create a custom encrypted field
class EncryptedField(models.BinaryField):
    """
    Custom field for AES encryption using Fernet (AES-128 CBC)
    """
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', True)
        super().__init__(*args, **kwargs)
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _get_or_create_key(self):
        """Get existing key or create a new one"""
        key_file = os.path.join(settings.BASE_DIR, '.encryption_key')
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            try:
                os.chmod(key_file, 0o600)
            except:
                pass
            return key
    
    def get_prep_value(self, value):
        if value is None:
            return None
        if not isinstance(value, str):
            value = str(value)
        encrypted_value = self.cipher.encrypt(value.encode())
        return encrypted_value
    
    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        try:
            decrypted_value = self.cipher.decrypt(value)
            return decrypted_value.decode()
        except Exception:
            return None
    
    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        try:
            decrypted_value = self.cipher.decrypt(value)
            return decrypted_value.decode()
        except Exception:
            return value


class EmployeeRecord(models.Model):
    """
    Employee financial record with encrypted sensitive data
    """
    employee_name = models.CharField(max_length=200, help_text="Employee's full name")
    department = models.CharField(max_length=100, help_text="Employee's department")
    
    # Sensitive fields - encrypted at rest
    bank_account_number = EncryptedField(help_text="Bank account number (encrypted)")
    annual_salary = EncryptedField(help_text="Annual salary (encrypted)")
    
    # Audit field
    added_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='added_employee_records',
        help_text="User who created this record"
    )
    
    # Metadata fields for better tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Employee Record"
        verbose_name_plural = "Employee Records"
    
    def __str__(self):
        # Don't include sensitive data in string representation
        return f"{self.employee_name} - {self.department} (Added by: {self.added_by.username})"
    
    def get_salary_display(self):
        """Helper method to display salary safely"""
        try:
            salary_value = self.annual_salary
            if salary_value:
                return f"${float(salary_value):,.2f}"
            return "Not set"
        except (ValueError, TypeError):
            return self.annual_salary
    
    def get_bank_account_display(self):
        """Helper method to display masked bank account"""
        try:
            if self.bank_account_number and len(str(self.bank_account_number)) > 4:
                account_str = str(self.bank_account_number)
                return f"****{account_str[-4:]}"
            return self.bank_account_number
        except Exception:
            return "[Encrypted]"

