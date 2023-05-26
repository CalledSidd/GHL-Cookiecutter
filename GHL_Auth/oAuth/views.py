from django.shortcuts import render
from django.views import View

# Create your views here.
class BaseView(View):
    template = 'auth.html'
    def get(self, request):
       code =  request.GET.get('code')
       print(code)
       context = {
           code : 'code'
       }
       return render(request, self.template, context)