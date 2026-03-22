# hr_vault/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import EmployeeRecord
from .forms import EmployeeRecordForm

@login_required(login_url='/admin/login/')
def add_employee(request):
    """
    View to add new employee record - only accessible to authenticated users
    """
    if request.method == 'POST':
        form = EmployeeRecordForm(request.POST)
        if form.is_valid():
            try:
                employee_record = form.save(commit=False)
                employee_record.added_by = request.user
                employee_record.save()
                messages.success(request, f'Successfully added employee record for {employee_record.employee_name}')
                return redirect('employee_list')
            except Exception as e:
                messages.error(request, f'Error saving record: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeRecordForm()
    
    context = {
        'form': form,
        'title': 'Add New Employee Record'
    }
    return render(request, 'hr_vault/add_employee.html', context)

@login_required(login_url='/admin/login/')
def employee_list(request):
    """
    View to list all employee records - only accessible to authenticated users
    """
    # Show all records for superusers, otherwise only their own
    if request.user.is_superuser:
        employees = EmployeeRecord.objects.all()
    else:
        employees = EmployeeRecord.objects.filter(added_by=request.user)
    
    # Prepare data for display with masked sensitive information
    employee_data = []
    for emp in employees:
        employee_data.append({
            'id': emp.id,
            'employee_name': emp.employee_name,
            'department': emp.department,
            'bank_account_number': emp.get_bank_account_display(),
            'annual_salary': emp.get_salary_display(),
            'added_by': emp.added_by.username,
            'created_at': emp.created_at
        })
    
    context = {
        'employees': employee_data,
        'total_count': employees.count(),
        'title': 'Employee Records'
    }
    return render(request, 'hr_vault/employee_list.html', context)

@login_required(login_url='/admin/login/')
def employee_detail(request, employee_id):
    """
    View to see detailed employee information
    """
    if request.user.is_superuser:
        employee = get_object_or_404(EmployeeRecord, id=employee_id)
    else:
        employee = get_object_or_404(EmployeeRecord, id=employee_id, added_by=request.user)
    
    context = {
        'employee': employee,
        'title': f'Employee Details: {employee.employee_name}'
    }
    return render(request, 'hr_vault/employee_detail.html', context)

@login_required(login_url='/admin/login/')
def edit_employee(request, employee_id):
    """
    View to edit employee record
    """
    if request.user.is_superuser:
        employee = get_object_or_404(EmployeeRecord, id=employee_id)
    else:
        employee = get_object_or_404(EmployeeRecord, id=employee_id, added_by=request.user)

    if request.method == 'POST':
        form = EmployeeRecordForm(request.POST, instance=employee)
        if form.is_valid():
            form.instance.added_by = request.user  # Ensure
            form.save()
            messages.success(request, f'Updated employee record for {employee.employee_name}')
            return redirect('employee_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeRecordForm(instance=employee)

    context = {
        'form': form,
        'title': f'Edit Employee: {employee.employee_name}'
    }
    return render(request, 'hr_vault/edit_employee.html', context)

@login_required(login_url='/admin/login/')
def delete_employee(request, employee_id):
    """
    View to delete employee record
    """
    if request.user.is_superuser:
        employee = get_object_or_404(EmployeeRecord, id=employee_id)
    else:
        employee = get_object_or_404(EmployeeRecord, id=employee_id, added_by=request.user)
    
    if request.method == 'POST':
        employee_name = employee.employee_name
        employee.delete()
        messages.success(request, f'Successfully deleted employee record for {employee_name}')
        return redirect('employee_list')
    
    context = {
        'employee': employee,
        'title': 'Confirm Delete'
    }
    return render(request, 'hr_vault/delete_employee.html', context)
