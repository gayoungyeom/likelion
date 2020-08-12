from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def sorry(request):
    return render(request, 'sorry.html')