from django.shortcuts import render
from django.views import View

from django.conf import settings

# Create your views here.
class BaseView(View):
    template = 'auth.html'
    def get(self, request):
       url = settings.GHL_URL
       print(url)
       code =  request.GET.get('code')
       print(code)
       context = {
           'code' : code,
           'url' : url
       }
       return render(request, self.template, context)