from django.shortcuts import render
from django.views import View

from django.conf import settings


from pprint import pprint

import requests

# Create your views here.
class BaseView(View):
    template = 'auth.html'

    def get_access_token(self, code):
        client_id = settings.CLIENT_ID
        client_secret = settings.CLIENT_SECRET
        location = settings.LOCATION
        print(location)
        
        access_url = 'https://services.leadconnectorhq.com/oauth/token'
        
        headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/x-www-form-urlencoded"
        }

        data = {
            "client_id" : client_id,
            "client_secret" : client_secret,
            "grant_type" : "authorization_code", #go and check the api calls in the website for the grant type
            "code" : code,
            "redirect_uri" : "http://localhost:8000/success"
        }
        
        
        access = requests.post(access_url, headers=headers, data=data)
        pprint(access.json())


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
    


def success(request):
    return render(request, 'succes.html')