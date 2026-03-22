from django.db import models
from django.contrib.auth.models import User

class EmployeeRecord(models.Model):
    employee_name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    bank_account_encrypted = models.TextField(blank=True)  # Encrypted bytes as base64 text
    salary_encrypted = models.TextField(blank=True)  # Encrypted bytes as base64 text
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee_name} - {self.department}"

