from django.conf.urls import url
from django.conf.urls import include
from django.urls import path
from vlab.lab import labviews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^mydevices/', labviews.mydevices, name='mydevices'),
    url(r'^myresearches', labviews.myresearches, name='myresearches')
    url(r'^mydocs', labviews.mydocs, name='mydocs'),
    url(r'^myorders', labviews.myorders, name='myorders'),
    url(r'^mybids', labviews.mybids, name='mybids'),
    url(r'^mysettings', labviews.mysettings, name='mysettings'),
    url(r'^mybookings', labviews.mysettings, name='mybookings'),
]
