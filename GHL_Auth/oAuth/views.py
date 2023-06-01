from django.shortcuts import render,redirect
from django.views import View

from django.conf import settings


from rest_framework.response import Response
from rest_framework.views import APIView

from . models import Api_Key_Data

import pprint

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
        return redirect('success')
    
    def success(request):
        return render(request, 'success.html')



# Validate Token Section End

# Get Contacts Endpoint 

class Contacts(APIView):
    template = 'contact.html'

    def get_custom_fields(self, id):
        pass

    def get(self, request):
        contact_id = request.GET.get('contact_id')
        auth = Api_Key_Data.objects.get(locationId = 'Fdjk8SCGrVjyXe1n09cE')
        token = auth.access_token
        contact_get = f'https://services.leadconnectorhq.com/contacts/{contact_id}'
        headers = {
            "Authorization" : f'Bearer {token}',
            "Version" : "2021-07-28",
            "Accept" : "application/json"
        }
        response = requests.get(contact_get, headers=headers)
        parsed_r = response.json()
        custField = parsed_r['contact']['customFields']
        custFieldId = custField[0]['id']
        if custFieldId:
            self.get_custom_fields(custFieldId)
        pprint_r = pprint.pformat(parsed_r)
        return Response(pprint_r)
    
