from django.shortcuts import render,redirect
from django.views import View

from django.conf import settings


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from . models import Api_Key_Data
from . pagination import ContactsPagination
from . serializers import ContactSerializer
from write import write_to_csv

import pprint

import requests
import json

# Create your views here.
# Validate Token Section
class AccessView(View):
    template = 'auth.html'
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    access_url = settings.ACCESS_URL
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    redirect_url = "http://localhost:8000/success"


    def success(request):
        return render(request, 'success.html')

    def get(self, request):
       url = settings.GHL_URL
       code =  request.GET.get('code')
       context = {
           'code' : code,
           'url' : url
       }
       return render(request, self.template, context)



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
                pprint.pprint(vals)
                data = obj
                obj.access_token = vals['access_token']
                obj.refresh_token = vals['refresh_token']
                obj.access_expires_in = vals['expires_in']
                data.save()
        except Exception as e :
                print(e, "Occured Exception at refresh")
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
            print(e, "Occured Exception at access")
            self.get_refresh_token(location)


    def post(self, request):
        try:
            location = request.POST["location"]
            code     = request.POST["code"]
            if location and code:
                self.get_access_token(code=code, location=location)
        except:
            return redirect(self.get)
        return redirect('success')
# Validate Token Section End

# Get Contacts Endpoint 

class Contact(APIView):
    template = 'contact.html'
    locationid = 'Fdjk8SCGrVjyXe1n09cE'
    auth = Api_Key_Data.objects.get(locationId = locationid)
    token = auth.access_token

    def get_custom_fields(self, id):
        headers = {
            "Authorization" : f'Bearer {self.token}',
            "Version" : "2021-07-28",
            "Accept" : "application/json"
        }
        cust_url = f'https://services.leadconnectorhq.com/locations/{self.locationid}/customFields/{id}'
        cust_res = requests.get(cust_url, headers=headers)
        field = cust_res.json()['customField']
        fieldName = field['name']
        print(fieldName)
        return fieldName


    def get(self, request):
        contact_id = request.GET.get('contact_id')
        auth = Api_Key_Data.objects.get(locationId = self.locationid)
        token = auth.access_token
        contact_get = f'https://services.leadconnectorhq.com/contacts/{contact_id}'
        headers = {
            "Authorization" : f'Bearer {token}',
            "Version" : "2021-07-28",
            "Accept" : "application/json"
        }
        response = requests.get(contact_get, headers=headers)
        parsed_r = response.json()
        pprint.pprint(parsed_r)
        if parsed_r:
            custField = parsed_r['contact']['customFields']
            for n in range(len(custField)):
                custFieldId = custField[n]['id']
                if custFieldId:
                    name = self.get_custom_fields(custFieldId)
                    parsed_r['contact']['customFields'][n]['id'] = name
            pprint_r = parsed_r
            return Response(pprint_r)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
class Contacts(APIView):
    locationid = 'w9LTt2jMahHxaA0vkl0r'
    
    auth = Api_Key_Data.objects.get(locationId = locationid)
    token = auth.access_token

    def get(self, request):
        contacts = []
        get_url = 'https://services.leadconnectorhq.com/contacts/'
        querystring = {'locationId' :self.locationid, "limit": 20}
        headers = {
            "Authorization": f'Bearer {self.token}',
            "Version": "2021-07-28",
            "Accept": "application/json"
        }
        count = 0
        first_response = requests.get(get_url, headers=headers, params=querystring)
        first_res_json = first_response.json()
        contacts += first_res_json.get('contacts')
        nexturl = first_res_json['meta'].get('nextPageUrl')
        print(nexturl)
        while True:     
            print(count)
            response = requests.get(nexturl, headers=headers)
            if response.status_code == 200:
                respone_json = response.json()
                contacts += respone_json.get('contacts')
                nexturl = respone_json['meta'].get('nextPageUrl') 
                if nexturl is None:
                    return Response(contacts)
            else:
                break
            count += 1
            if contacts:
                write_to_csv(contacts)
        return Response(contacts)