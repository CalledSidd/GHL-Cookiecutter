from django.urls import path
from . views import BaseView, Contacts


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('success', BaseView.success),
    path('contact',Contacts.as_view(), name='contacts')
]