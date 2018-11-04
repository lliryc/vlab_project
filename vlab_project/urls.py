"""vlab_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from vlab import views
from vlab.lab import labviews
from django.conf import settings
from django.conf.urls.static import static
from vlab.views import OrgUserRegistrationView
from vlab.forms import OrgUserRegistrationForm
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^researches/', views.researches, name='researches'),
    url(r'^auctions/', views.auctions, name='auctions'),
    url(r'^problems/', views.problems, name='problems'),
    url(r'^labs/', views.labs, name='labs'),

    url(r'^lab/',include('vlab.lab.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^accounts/register/$', OrgUserRegistrationView.as_view(form_class=OrgUserRegistrationForm), name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^new_organization/', views.new_organization, name='new_organization'),
    url(r'^captcha/', include('captcha.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
