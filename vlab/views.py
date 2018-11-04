from django.shortcuts import render, redirect, reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from registration.backends.default.views import RegistrationView
from registration.models import RegistrationProfile
from registration import signals
from itertools import groupby

from vlab.forms import OrgUserRegistrationForm, OrgForm
from vlab.models import OrgUser, LabInfo, MapCache
from datetime import datetime
import json
# import pdb; pdb.set_trace()

# Create your views here.
def index(request):
    context_dict = {}
    return render(request, 'vlab/index.html', context = context_dict)

def auctions(request):
    context_dict = {}
    return render(request, 'vlab/auctions.html', context = context_dict)

def labs(request):
    lab_infos = LabInfo.objects.all()

    grouped_dict = {}

    for lab_info in lab_infos:
        key = (lab_info.base_org_title.replace('\n',''), lab_info.base_org_address.replace('\n',''), lab_info.geocode)

        if key not in grouped_dict:
             x_str, y_str = lab_info.geocode.split(',')
             x, y = float(x_str), float(y_str)
             grouped_dict[key] = {'labs': [], 'base_org_title': lab_info.base_org_title.replace('\n',''), 'base_org_address': lab_info.base_org_address.replace('\n',''), 'geocode': [x,y]}

        devices = [di.title.replace('\n','') for di in  lab_info.deviceinfo_set.all()]

        print(devices)

        grouped_dict[key]['labs'].append({'title': lab_info.title.replace('\n',''), 'devices': devices})

    grouped_data = json.dumps(list(grouped_dict.values()), ensure_ascii=False)

    #for key, group in groupby(lab_infos, lambda x: (x['base_org_title'].replace('\n',''), x['base_org_address'], x['geocode'])):
    #    grouped_dict[key] = len(list(group))
    #    print(key)
    #    print(len(list(group)))
    #print(grouped_dict)
    context_dict = {'lab_data': grouped_data}
    return render(request, 'vlab/labs.html', context = context_dict)

def problems(request):
    context_dict = {}
    return render(request, 'vlab/problems.html', context = context_dict)

def researches(request):
    context_dict = {}
    return render(request, 'vlab/researches.html', context = context_dict)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/account')
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(form.errors)
    else:
        form = UserCreationForm()

    # Render the template depending on the context.
    return render(request, 'registration/registration_form.html',
        {'form': form,
        'registered': registered})

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your vlab account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
            # The request is not a HTTP POST, so display the login form.
            # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'registration/login.html', {})

# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))

def new_organization(request):
    if request.method == 'POST':
        form = OrgForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/accounts/register')
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(form.errors)
    else:
        form = OrgForm()
    return render(request, 'vlab/new_organization.html',{'form': form})


class OrgUserRegistrationView(RegistrationView):
    form_class = OrgUserRegistrationForm

    def form_valid(self, form):
        # self.object = form.save(commit=False)
        # self.object.set_unusable_password()
        # self.object.is_active = True
        # self.object.save()
        #
        # form = forms.RegistrationEmailForm(self.object, self.request.POST)
        # form.is_valid()
        form.is_valid()
        print(form.errors)
        res = super().form_valid(form)
        print(form.errors)
        return res

    # def register(self, request, form):
    #
    #     site = get_current_site(request)
    #
    #     if hasattr(form, 'save'):
    #         print(form)
    #         new_user_instance = form.save()
    #     else:
    #         new_user_instance = (OrgUser().objects
    #                              .create_user(**form.cleaned_data))
    #
    #     new_user = RegistrationProfile.objects.create_inactive_user(
    #         new_user=new_user_instance,
    #         site=site,
    #         send_email=self.SEND_ACTIVATION_EMAIL,
    #         request=request,
    #     )
    #     signals.user_registered.send(sender=self.__class__,
    #                                  user=new_user,
    #                                  request=request)
    #     return new_user
