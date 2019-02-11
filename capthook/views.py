import datetime
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.models import User
from rest_hooks.models import Hook
from rest_hooks.signals import raw_hook_event
from .models import Employee
from .forms import EmployeeForm


def all_employees(request):
    if request.method == 'GET':
        print(dir(Hook))
        all_employees = Employee.objects.all()
        return render(request, 'all_employees.html', {'all_employees': all_employees})


def add_employee(request):
    if request.method == 'GET':
        form = EmployeeForm()
    else:
        form = EmployeeForm(request.POST)
        if form.is_valid():
            user = User.objects.all().first()
            name = form.cleaned_data.get('name')
            hometown = form.cleaned_data.get('hometown')
            form.save()
            print(dir(Hook))
            hook = Hook(
                user=user,
                event='employee.added',
                target='http://localhost/target.php')
            hook.save()
            # user = Employee.objects.filter(name=name).first()
            # raw_hook_event.send(
            #     sender=None,
            #     event_name='emp.created',
            #     payload={
            #         'name': name,
            #         'hometown': hometown,
            #         'when': datetime.datetime.now().isoformat()
            #     },
            #     user=user
            # )
            form = EmployeeForm()
            # redirect(reverse('capthook:target'))
        else:
            print(form.errors)
    return render(request, 'add_employee.html', {'form': form})


def update_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    form = EmployeeForm(request.POST or None, instance=employee)
    if form.is_valid():
        form.save()
        return redirect('capthook:all')
    return render(request, 'update_employee.html', {'form': form})


def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        employee.delete()
        return redirect('capthook:all')
    return render(request, 'delete_employee.html', {'employee': employee})


# def add_employee_event(request):



