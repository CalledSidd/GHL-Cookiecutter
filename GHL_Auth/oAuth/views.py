from django.shortcuts import render,redirect
from django.views import View

from django.conf import settings


from . models import Api_Key_Data

from pprint import pprint

import requests
import json

# Create your views here.
class BaseView(View):
    template = 'auth.html'

    def get_access_token(self, code, location):
        client_id = settings.CLIENT_ID
        client_secret = settings.CLIENT_SECRET
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
        vals = access.json()
        pprint(vals)
        print(vals['access_token'])
        try:
            data = Api_Key_Data(
                access_token = vals['access_token'],
                companyId = vals['companyId'],
                access_expires_in = vals['expires_in'],
                locationId = vals['locationId'],
                refresh_token = vals['refresh_token'],
            )
        except Exception as e:
            print(e, "This is the occured exception")
            data = Api_Key_Data.objects.get(location = location)
            data.refresh_token = vals['refresh_token']
            return redirect(self.get)
        data.save()



    def get(self, request):
       url = settings.GHL_URL
       code =  request.GET.get('code')
       context = {
           'code' : code,
           'url' : url
       }
       return render(request, self.template, context)
    
    def post(self, request):
        try:
            location = request.POST["location"]
            code     = request.POST["code"]
            if location and code:
                self.get_access_token(code=code, location=location)
        except:
            return redirect(self.get)
        return redirect(success)
    


def success(request):
    return render(request, 'success.html')