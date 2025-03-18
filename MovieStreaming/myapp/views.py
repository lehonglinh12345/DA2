from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from .models import Movie

def home(request):
  
    return render(request, "myapp/home.html")



def gioithieu(request):
    return render(request, 'myapp/gioithieu.html')