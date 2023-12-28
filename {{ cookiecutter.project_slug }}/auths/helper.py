from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from . models import Authtokendata 

import requests

def generate_url():
    url = "{BASE}/oauth/chooselocation?response_type=code&redirect_uri={REDIRECT_URI}&client_id={CLIENT_ID}&scope={SCOPE}".format(BASE = settings.BASE,REDIRECT_URI=settings.REDIRECT_URL,CLIENT_ID=settings.CLIENT_ID,SCOPE=" ".join(settings.SCOPE))
    return url


def custom_requests(locationId, method, url, data=None, params=None):
    try:
        location = Authtokendata.objects.get(locationId = locationId)
    except Authtokendata.DoesNotExist:
        return {"status_code" : 400, "text": "No such location Onboarded"}
    current = timezone.now()
    expiry = location.created_at + timedelta(seconds=location.access_expires_in)
    access_token = location.access_token
    if expiry < current:
        print("TOKEN IS EXPIRED")
        auth_url = settings.ACCESS_URL
        data = {
            'client_id' : settings.CLIENT_ID,
            'client_secret' : settings.CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token' : location.refresh_token
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        response = requests.post(auth_url, data=data, headers=headers)
        if response.status_code != 200:
            return {"data": response.json(), "status_code" : response.status_code, "text": response.text}
        response_data = response.json()
        location.access_token = response_data['access_token']
        location.refresh_token = response_data['refresh_token']
        location.access_expires_in = response_data['expires_in']
        location.created_at = timezone.now()
        location.save(update_fields=['access_token', 'refresh_token', 'access_expires_in', 'created_at'])
        access_token = response_data['access_token']

    headers = {
        "Authorization" : f'Bearer {access_token}',
        "Version": "2021-07-28",
        "Accept": "application/json"
    }
    if method == "POST":
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            return {"data": response.json(), "status_code" : response.status_code, "text": response.text}
        return {"data": response.json(), "status_code" : response.status_code, "text": response.text}
    elif method == "GET":
        print("IN HELPERS get")
        response = requests.get(url, headers=headers, params=params)
        print(response.status_code)
        if response.status_code != 200:
            return {"data": response.json(), "status_code" : response.status_code, "text": response.text}
        return {"data": response.json(), "status_code" : response.status_code, "text": response.text}