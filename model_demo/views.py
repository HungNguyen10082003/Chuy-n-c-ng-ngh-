from django.shortcuts import render
from .models import Item

def homepage(request):
    items = Item.objects.filter(status='live')
    return render(request, 'home.html', {'items': items})
