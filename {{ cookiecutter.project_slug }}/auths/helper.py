from django.conf import settings

def generate_url():
    url = "{BASE}/oauth/chooselocation?response_type=code&redirect_uri={REDIRECT_URI}&client_id={CLIENT_ID}&scope={SCOPE}".format(BASE = settings.BASE,REDIRECT_URI=settings.REDIRECT_URL,CLIENT_ID=settings.CLIENT_ID,SCOPE=" ".join(settings.SCOPE))
    return url

def custom_requests():
    pass