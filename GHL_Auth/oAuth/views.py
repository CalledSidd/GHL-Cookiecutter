from django.shortcuts import render,redirect
from django.views import View

from django.conf import settings


from . models import Api_Key_Data

from pprint import pprint

import requests
import json

# Create your views here.
# Validate Token Section
class BaseView(View):

    template = 'auth.html'

    client_id = settings.CLIENT_ID

    client_secret = settings.CLIENT_SECRET

    access_url = settings.ACCESS_URL

    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    redirect_url = "http://localhost:8000/success"


    def get_refresh_token(self, location):
        try:
            obj = Api_Key_Data.objects.get(locationId = location)
            if obj:
                print(type(obj.refresh_token))
                data = {
                    "client_id" : self.client_id,
                    "client_secret" : self.client_secret,
                    "grant_type" : "refresh_token",
                    "refresh_token" : obj.refresh_token,
                    "redirect_uri" : self.redirect_url,
                }
                refresh = requests.post(self.access_url, headers=self.headers, data=data)
                vals = refresh.json()
                pprint(vals)
                data = obj
                obj.access_token = vals['access_token']
                obj.refresh_token = vals['refresh_token']
                obj.access_expires_in = vals['expires_in']
                data.save()
        except Exception as e :
                return redirect(self.get)


    def get_access_token(self, code, location):
        data = {
            "client_id" : self.client_id,
            "client_secret" : self.client_secret,
            "grant_type" : "authorization_code", 
            "code" : code,
            "redirect_uri" : self.redirect_url
        }        
        
        access = requests.post(self.access_url, headers=self.headers, data=data)
        vals = access.json()
        try:
            data = Api_Key_Data(
                access_token = vals['access_token'],
                companyId = vals['companyId'],
                access_expires_in = vals['expires_in'],
                locationId = vals['locationId'],
                refresh_token = vals['refresh_token'],
            )
            data.save()
        except Exception as e:
            self.get_refresh_token(location)


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
        return redirect(self.success)
    
    def success(request):
        return render(request, 'success.html')



# Validate Token Section End

# Get Contacts Endpoint 

class Contacts(View):
    template = 'contact.html'
    def get(self, request):
        contact_id = request.GET.get('contact_id')
        print(contact_id)
        return render(request, self.template)