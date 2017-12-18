from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^tracks', IndexView.as_view(), name='index'),
]
