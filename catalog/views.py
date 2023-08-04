from django.shortcuts import render
from builtins import *
# Create your views here.


def home(request):
    return render(request, 'main/home.html')


def contacts(request):
    if request == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name}, {phone}, ({message})')
    return render(request, 'main/contacts.html')