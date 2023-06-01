from django.urls import path
from . views import AccessView, Contact, Contacts


urlpatterns = [
    path('', AccessView.as_view()),
    path('success', AccessView.success),
    path('get_contact/',Contact.as_view()),
    path('contacts',Contacts.as_view()),
]