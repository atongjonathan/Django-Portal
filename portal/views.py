from django.shortcuts import render
from django.urls import path
from . import views
from django.http import HttpResponse

def index(request):
    return render(request, template_name="portal/index.html")


def test(request):
    return render(request, 'portal/test.html')