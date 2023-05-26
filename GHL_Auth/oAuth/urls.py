from django.urls import path
from . views import BaseView, success


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('success', success)
]