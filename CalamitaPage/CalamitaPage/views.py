from django.http import HttpResponse
from django.shortcuts import render

def index(request): #primera vista
    
    return render(request,"CalamitaPage/index.html")











