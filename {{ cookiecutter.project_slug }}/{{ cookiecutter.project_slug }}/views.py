from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings


import requests

from auths.models import Authtokendata

class Onboarding(View):
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
        template = 'get.html'
        url = settings.GHL_URL
        code = request.GET.get('code')
        context = {
            'code' : code, 
            'url' : url,
        }
        return render(request, template, context)

    def post(self, request):
        try:
            location = request.POST['location']
            code = request.POST['code']
            if location and code:
                self.get_access_token(code=code, location=location)
        except:
            return redirect(self.get)
        return redirect('success')

    def get_access_token(self, code, location):
        data = {
            "client_id" : self.client_id,
            "client_secret" : self.client_secret,
            "grant_type" : "authorization_code",
            "code" : code,
            "redirect_uri" : self.redirect_url
        }
        access = requests.post(self.access_url, headers=self.headers, data=data)
        response = access.json()
        try:
            data = Authtokendata(
                access_token = response['access_token'],
                companyId = response['companyId'],
                access_expires_in = response['expires_in'],
                locationId = response['locationId'],
                refresh_token = response['refresh_token'],
            )
            data.save()
        except Exception as e:
            print(e)
            self.get_refresh_token(location)

    def get_refresh_token(self, location):
        try:
            token_data = Authtokendata.objects.get(locationId = location)
            if token_data:
                data = {
                    "client_id" : self.client_id,
                    "client_secret" : self.client_secret,
                    "grant_type" : "refresh_token",
                    "refresh_token" : token_data.refresh_token,
                    "redirect_uri" : self.redirect_url,
                }
                refresh = requests.post(self.access_url, headers=self.headers, data=data)
                response = refresh.json()
                token_data.access_token = response['access_token']
                token_data.refresh_token = response['refresh_token']
                token_data.access_expires_in = response['expires_in']
                token_data.save()
        except Exception as e:
            print(e)
            return redirect(self.get)