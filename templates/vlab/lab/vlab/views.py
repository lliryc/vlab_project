from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from models import LabInfo, MapCache
from datetime import datetime
# import pdb; pdb.set_trace()

# Create your views here.
def index(request):
    context_dict = {}
    return render(request, 'vlab/index.html', context = context_dict)

def auctions(request):
    context_dict = {}
    return render(request, 'vlab/auctions.html', context = context_dict)

def labs(request):
    context_dict = {}
    return render(request, 'vlab/labs.html', context = context_dict)

def problems(request):
    context_dict = {}
    return render(request, 'vlab/problems.html', context = context_dict)

def researches(request):
    context_dict = {}
    return render(request, 'vlab/researches.html', context = context_dict)
