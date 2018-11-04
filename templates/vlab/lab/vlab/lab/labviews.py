from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
# import pdb; pdb.set_trace()

# Create your views here.
def index(request):
    context_dict = {}
    return render(request, 'vlab/lab/mydevices.html', context = context_dict)

def mydevices(request):
    context_dict = {}
    return render(request, 'vlab/lab/mydevices.html', context = context_dict)

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
