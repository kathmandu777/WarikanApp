from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(req):
    return HttpResponse('Hello World')

def food(request):
    return HttpResponse('This is food page.')

def who(request):
    return HttpResponse('This is who page.')

def result(request):
    return HttpResponse('This is result page.')