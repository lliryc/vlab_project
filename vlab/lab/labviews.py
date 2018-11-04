from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from vlab.forms import DeviceForm
from vlab.models import Device, Org, OrgUser
# import pdb; pdb.set_trace()

# Create your views here.
def index(request):
    context_dict = {}
    return render(request, 'vlab/lab/mydevices.html', context = context_dict)

def mydevices(request):
    context_dict = {}
    return render(request, 'vlab/lab/mydevices.html', context = context_dict)

def mydevices_add(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('/lab/mydevices/')
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(form.errors)
    else:
        form = DeviceForm(initial={'lab': OrgUser.objects.all()[:1].get(), 'broken': True})
    return render(request, 'vlab/lab/mydevices_add.html',{'form': form})


def myresearches(request):
    context_dict = {}
    return render(request, 'vlab/lab/myresearches.html', context = context_dict)

def mybids(request):
    context_dict = {}
    return render(request, 'vlab/lab/mybids.html', context = context_dict)

def myorders(request):
    context_dict = {}
    return render(request, 'vlab/lab/myorders.html', context = context_dict)

def mydocs(request):
    context_dict = {}
    return render(request, 'vlab/lab/mydocs.html', context = context_dict)

def mysettings(request):
    context_dict = {}
    return render(request, 'vlab/lab/mysettings.html', context = context_dict)

def myqualifications(request):
    context_dict = {}
    return render(request, 'vlab/lab/myqualifications.html', context = context_dict)

def myqualifications_add(request):
    context_dict = {}
    return render(request, 'vlab/lab/myqualifications_add.html', context = context_dict)

def mydevices_qualification(request):
    context_dict = {}
    return render(request, 'vlab/lab/mydevices_qualification.html', context = context_dict)

def mydevices_qualification_add(request):
    context_dict = {}
    return render(request, 'vlab/lab/mydevices_qualification_add.html', context = context_dict)
