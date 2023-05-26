from django.shortcuts import render
from django.views import View

from django.conf import settings

import requests

# Create your views here.
class BaseView(View):
    template = 'auth.html'

    def get_access_token(self, code):
        client_id = settings.CLIENT_ID
        client_secret = settings.CLIENT_SECRET
        location = settings.LOCATION
        
        access_url = 'https://services.leadconnectorhq.com/oauth/token'
        
        headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/x-www-form-urlencoded"
        }
        
        
        
        access = requests.post(access_url)


    def get(self, request):
       url = settings.GHL_URL
       code =  request.GET.get('code')
       if code:
           self.get_access_token(code)
       context = {
           'code' : code,
           'url' : url
       }
       return render(request, self.template, context)