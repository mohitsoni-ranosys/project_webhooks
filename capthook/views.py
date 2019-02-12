import datetime
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.models import User
from rest_hooks.models import Hook
from rest_hooks.signals import raw_hook_event

import hashlib
import hmac
# import httplib
import http.client
import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

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

def handle_webhook(event, payload):
    """Simple webhook handler that prints the event and payload to the console"""
    print('Received the {} event'.format(event))
    print(json.dumps(payload, indent=4))


@csrf_exempt
def handle_github_hook(request):
    # Check the X-Hub-Signature header to make sure this is a valid request.
    # github_signature = request.META['HTTP_X_HUB_SIGNATURE']
    print(request.META)
    print(request.META.get('HTTP_X_HUB_SIGNATURE'))
    github_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
    signature = hmac.new(settings.GITHUB_WEBHOOK_SECRET, request.body, hashlib.sha1)
    expected_signature = 'sha1=' + signature.hexdigest()
    # if not hmac.compare_digest(github_signature, expected_signature):
    #     return HttpResponseForbidden('Invalid signature header')

    # Sometimes the payload comes in as the request body, sometimes it comes in
    # as a POST parameter. This will handle either case.
    if 'payload' in request.POST:
        payload = json.loads(request.POST['payload'])
    else:
        print("*******************************")
        print(request.body)
        print('------------------------')
        print(request.POST)
        print("*******************************")
        payload = json.loads(request.body)

    event = request.META['HTTP_X_GITHUB_EVENT']

    # This is where you'll do something with the webhook
    handle_webhook(event, payload)

    return HttpResponse('Webhook received', status=http.client.ACCEPTED)

